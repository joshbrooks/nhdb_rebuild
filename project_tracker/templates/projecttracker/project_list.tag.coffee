window.project_list_tag = this
self = this

self.pagesize = 20
self.page = 1
self.query={}

self.on 'mount', () ->
  self.message = "Projects"
  self.projects = []


  RiotControl.on 'projects_changed', (projects) ->
    self.projects = projects
    self.update()

RiotControl.on 'load_projects', (query) ->
  self.query=query
  $('project-list').show()
  $('project-detail').hide()


self.paginate = (projects) ->
  from = self.page * self.pagesize
  to = from + self.pagesize
  r = projects.slice( from , to )
  return r

self.filter = (projects) ->

  if self.query.text
    projects.filter (project) ->
      project.name.toUpperCase().indexOf(self.query.text.toUpperCase()) != -1
#
  if self.query.status
    console.log self.query.status
    projects = projects.filter (project) ->
      return true if project.status.toUpperCase() is self.query.status.toUpperCase()
    console.log projects.length
  return projects

self.set_page = (e) ->
  self.page = parseInt($(e.target).attr('data-set-page'))
  self.update()

self.project_detail = (e) ->
  riot.route "/project/by-id/#{e.item.id}"
  RiotControl.trigger('load_project_detail', e.item)

sr = riot.route.create()
sr '/project..', () ->
  RiotControl.trigger('load_projects', riot.route.query())

sr '/project/by-id/*', (project_id) ->

self.trans = (translation_id) ->
  # return translation_id
  return translationstore.strings[translation_id].translation['name_tet']