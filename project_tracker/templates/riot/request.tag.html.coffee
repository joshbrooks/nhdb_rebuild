### RequestTag coffeescript/js code ###

self = this
self.message = 'Requests'
self.online_status = 'online'
self.requestCounts = {}
self.requests = []

### Just test if our store is available ###
self.ping = (e) ->
  console.log 'ping'
  console.log e

### Update requestCounts, a hash of request properties, with the number of requests meeting criteria ###
self.requestStats = (fieldname) ->
  r = {}
  for request in self.requests
    value = request[fieldname] or 'undefined'
    r[value] = (r[value] or 0) + 1
  self.requestCounts[fieldname] = r

### Upon mounting this tag, retrieve requests from localStorage ###
self.on 'mount', -> RiotControl.trigger 'unshelve_requests'

RiotControl.on 'requests_changed', (requests) ->
  self.requests = requests
  console.log requests
  # Attempt to request_do any requests which have not been responded to yet and have a parameter "action = immediate"
  # This allows optional caching dependent on a request parameter
  for request in requests
    # Override api if weAreLive is
    console.log request.action

    if request.action is 'immediate' and request.status is 0
      request.action = 'inprogress'
      RiotControl.trigger 'request_do', request

  self.requestStats('status')
  self.requestStats('method')
  self.requestStats('modelName')
  self.update()

RiotControl.on 'request_failed', (request, jqXHR, textStatus, errorThrown) ->
  request.status = jqXHR.status
  self.update()
  console.log jqXHR
  console.log textStatus
  console.log errorThrown

RiotControl.on 'request_add', -> self.update()


### Show requests with only a give status or method ###
self.updateFiltering = ->
  filter = $(self.filtering).val()
  RiotControl.trigger('updateRequestFiltering', filter)

self.clearRequests = ->
  filter = $(self.clearing).val()
  console.log('clearRequests')
  console.log(filter)
  RiotControl.trigger('clearRequests', filter)

self.showAllRequests = -> self.setPropertyByPropertyRange 'status', -1, -1, 'hidden'

self.doAllRequests = ->
  console.log('doAllRequests')
  for request in self.requests
    if not (200 < request.status <= 400)
      RiotControl.trigger 'request_do', request

### Functions which can be provided by the tag as events, ie onclick={ ... }###

self.request_do = (e) -> RiotControl.trigger 'request_do', e.item
self.request_remove = (e) -> RiotControl.trigger 'request_remove', e
self.shelve_requests = ->  RiotControl.trigger 'shelve_requests'
self.unshelve_requests = -> RiotControl.trigger 'unshelve_requests'
self.clearSuccessfulRequests = -> self.requests = self.requests.filterByPropertyRange 200, 300
self.clearBadRequests = -> self.requests = self.requests.filterByPropertyRange 400, 500

# ---
# generated by js2coffee 2.2.0