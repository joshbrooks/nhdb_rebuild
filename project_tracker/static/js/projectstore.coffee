window.ProjectStore = (projects) ->

  riot.observable this
  self = this
  self.projects = projects || []

  self.on 'load_projects', () ->
    url = Urls['nhdb:project_data']('json')
    request = $.get(url)
    request.done ()->
      self.projects = request.responseJSON
      self.trigger 'projects_changed', self.projects
