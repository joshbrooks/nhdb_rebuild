self = this
self.message = "Projects"
self.projects = []

self.edit_project = (e) ->
  riot.route "project/#{this.id}/detail"
  RiotControl.trigger 'load_project_detail', this

self.on 'mount', ->
  return

RiotControl.on 'projects_changed', (projects, page, count, page_size) ->
  self.projects = projects
  self.page = page
  self.page_size = page_size
  self.count = count
  self.pages = Math.ceil(self.count/self.page_size)

  console.log(self)

  console.log('update')
  self.update()

self.set_page = (e) ->
  page = $(e.target).attr('data-set-page')
  opts =
    page:page or 1
    per_page:50
    filters:$('form#project-filter').serialize()
  RiotControl.trigger('projects_reload', opts)

self.ping = () ->
  alert('ping')

ping = () ->
  alert('ping')
