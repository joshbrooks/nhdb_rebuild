modelName = 'project'
appName = 'projecttracker'


window.ProjectStore = (projects) ->

  riot.observable this
  self = this
  self.projects = projects || []
  self.edit = {} # Store the Person currently being edited
  self.filters = ''

  ### Request the latest projects from DRF ###
  self.on 'projects_reload', (opts)->
    opts = opts or {}
    page = opts.page or 1
    per_page = opts.per_page or 100
    filters = opts.filters or ''
    self.filters = filters

    request =
      'url': "/#{ appName }/api/#{ modelName }/?page_size=#{per_page}&page=#{page}&#{filters}"
      'method': 'GET'
      'data': ''
      'status': 0
      'done': 'projects_reload_done'
      'action': 'immediate' # See RequestStore implementation: this indicates "do not cache me"
      'fail': 'projects_reload_from_server_fail'

    RiotControl.trigger 'request_add', request

  self.on 'projects_reload_done', (data, textStatus, jqXHR) ->
    self.projects = data.results
    self.trigger 'projects_changed', self.projects, data.page, data.count, data.page_size
#    self.trigger 'reset_pagination', data.count, data.page, data.pages


  self.on 'ping', ->
    alert 'ping'

  self.on 'tag_selected', (e) ->
    console.log e
