###
RequestStore
  Provides a riotjs store to hold/inspect request information before it is passed to the server, and
  store results afterwards

  Properties of a request:
  url = URL to call
  method = "GET", "POST", "PUT" or "DELETE"
  data = JSON content for the request

  The following jQuery promises can be passed (as RiotControl function names):
  always = a RiotControl function name to call whatever happens
  done = a RiotControl function name to call on success
  fail = a RiotControl function name to call on failure
###


window.RequestStore = ->
  # Holds details of an AJAX request: provides a local history of changes which we submit to the server
  riot.observable this
  self = this
  @requests = []
  storename = 'RequestStore'

  ### Read the current csrf token ###
  getCookie = (name) ->
    cookieValue = null
    if document.cookie and document.cookie != ''
      cookies = document.cookie.split(';')
      i = 0
      while i < cookies.length
        cookie = jQuery.trim(cookies[i])
        # Does this cookie string begin with the name we want?
        if cookie.substring(0, name.length + 1) == name + '='
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        i++
    cookieValue

  getCsrftoken = ->
    getCookie 'csrftoken'

  ### This is beautiful coffeescript ###
  Array::removing = (fieldname, fieldvalue) -> x for x in @ when not (x[fieldname] == fieldvalue )


  ### list.filterHighLow('status', 200, 400) -> new list where all items have 'status' property between 200 and 399 ###
  Array::filterByPropertyRange = (propertyToRead, low, high) -> x for x in @ when low <= x[propertyToRead] < high

  ###
    list.setPropertyByPropertyRange ('status', 200, 400, 'hidden') -> new list where if "status" is between 200 and 400, hidden = true
    otherwise hidden is set to false
  ###
  @setPropertyByPropertyRange = (propertyToRead, low, high, propertyToSet, inverse) ->
    console.log ("#{propertyToRead}, #{low},#{ high}, #{propertyToSet}, #{inverse}")
    for x in @requests
      if inverse is 'false'
        x[propertyToSet] = if (low <= x[propertyToRead] < high) then false else true
      else
        x[propertyToSet] = if (low <= x[propertyToRead] < high) then true else false
    return false

  ###
    filterByPropertyValue ('method', 'PUT', 'filter_by_method') -> set filter_by_method = true only if 'method' is 'PUT'
  ###
  @filterByPropertyValue = (propertyToRead, valueToTest, propertyToSet, inverse) ->
    for x in @requests
      if inverse is 'false'
        x[propertyToSet] = if (x[propertyToRead] is valueToTest) then false else true
      else
        x[propertyToSet] = if (x[propertyToRead] is valueToTest) then true else false
    return false


  @on 'ping', ->
    console.log 'ping'

  ### Shelve / unshelve requests to local storage to persist them through a browser restart
    TODO: Make this work with Lawnchair not just localstorage
  ###

  @on 'shelve_requests', ->
    localStorage.setItem 'requests', JSON.stringify(@requests)

  @on 'unshelve_requests', ->
    @requests = JSON.parse(localStorage.getItem('requests')) or []
    # Clear present items in the page
    RiotControl.trigger 'requests_changed', @requests

  @on 'requests_init', ->
    @trigger 'requests_changed', @requests

  @on 'request_remove', (e) ->
    i = @requests.length - 1
    while i >= 0
      if @requests[i] == e.item
        @requests.splice i, 1
      i--
    RiotControl.trigger 'requests_changed', @requests

  @on 'request_add', (request) ->
    request.fail = request.fail or 'request_failed' # This is a Riotcontrol function to call on failure
    request.status = request.status or 0
    @requests.push request
    RiotControl.trigger 'requests_changed', @requests

  @on 'request_update', (item, xhr) ->
    item.status = parseInt(xhr.status)
    @trigger 'requests_changed', @requests

  @on 'updateRequestFiltering', (filter_value) ->
    # HTTP response codes

    request.hidden = false for request in @requests if filter_value is 'all'
    if filter_value is 'waiting'
      for request in @requests
        request.hidden = if (filter_value is 'waiting' and (request.status is undefined or request.status is 0)) then false else true

    @setPropertyByPropertyRange 'status', 200, 300, 'hidden', 'false' if filter_value is 'success'
    @setPropertyByPropertyRange 'status', 400, 500, 'hidden', 'false' if filter_value is 'failed'

    # HTTP methods
    @filterByPropertyValue 'method', 'PUT', 'hidden', 'false' if filter_value is 'put'
    @filterByPropertyValue 'method', 'GET', 'hidden', 'false'  if filter_value is 'get'
    @filterByPropertyValue 'method', 'POST', 'hidden', 'false'  if filter_value is 'post'
    @filterByPropertyValue 'method', 'DELETE', 'hidden', 'false'  if filter_value is 'delete'

  @on 'clearRequests', (filter_value) ->
    # TODO:  Ugly mix of prototype and functions here
    console.log("clearRequests #{filter_value}")
    @requests.filterByPropertyRange 'status', 200, 300 if filter_value is 'success'
    @requests.filterByPropertyRange 'status', 400, 500 if filter_value is 'failed'
    @requests = [] if filter_value is 'all'

    @requests = @requests.removing('method', 'GET') if filter_value is 'get'
    @requests = @requests.removing('method', 'POST') if filter_value is 'post'
    @requests = @requests.removing('method', 'DELETE') if filter_value is 'delete'

    RiotControl.trigger('requests_changed', @requests)


  ### Attempt to send our request to the server ###
  @on 'request_do', (request) ->
    headers =
      'Accept': 'application/json; q=1.0, */*'
      'X-CSRFToken': getCsrftoken()
    xhr = $.ajax(
      url: request.url
      method: request.method
      data: request.data
      contentType: 'application/json'
      processData: false
      headers: headers)

    ### Always update our riotjs store instance with the response code ###
    xhr.done (data, textStatus, jqXHR) ->
      # Passing a function is not suitable for storage -use a named RiotControl function instead
      if $.isFunction(request.done)
         console.error  'This will break localstorage for requests!'
         request.done data, textStatus, jqXHR
      if typeof request.done == 'string'
        console.log "[#{storename}] request_do -> #{request.done}"
        RiotControl.trigger request.done, data, textStatus, jqXHR, request
      # Remove on successful completion if the request type is GET
      if ( 200 <= jqXHR.status <= 400 ) and request.method is 'GET'
        console.log 'test for remove: if ( 200 <= jqXHR.status <= 400 ) and request.method is "GET"'
#        RiotControl.trigger('request_remove', {item: request})


    ### Always update our riotjs store instance with the response code ###
    xhr.always (data, textStatus, jqXHR) ->
      RiotControl.trigger 'request_update', request, jqXHR
      RiotControl.trigger 'requests_changed', @requests

      if typeof request.always == 'string'
        RiotControl.trigger request.always, data, textStatus, jqXHR, request

    xhr.fail (jqXHR, textStatus, errorThrown) ->
      if typeof request.fail == 'string'
        RiotControl.trigger request.fail, request, jqXHR, textStatus, errorThrown



  ### Adding a new model to the DRF ###
  @on 'model_add', (modelData, appName, modelName, done) ->
    url = '/' + appName + '/api/' + modelName + '/'
    RiotControl.trigger 'request_add',
      'url': url
      'method': 'POST'
      'data': modelData
      'done': done


  ### Prepare a request to delete a model instance through DRF  ###
  @on 'model_remove', (appName, modelName, modelPk, done) ->
    url = '/' + appName + '/api/' + modelName + '/' + modelPk + '/'
    RiotControl.trigger 'request_add',
      'url': url
      'method': 'DELETE'
      'data': ''
      'done': done
      'modelPk': modelPk
      'modelName': modelName
      'appName': appName


  ### Prepare a request to update a model instance through DRF ###
  @on 'model_update', (modelData, appName, modelName, modelPk, done, opts) ->
    url = '/' + appName + '/api/' + modelName + '/' + modelPk + '/'
    RiotControl.trigger 'request_add',
      'url': url
      'method': 'PUT'
      'data': modelData
      'done': done
      'modelPk': modelPk
      'modelName': modelName
      'appName': appName