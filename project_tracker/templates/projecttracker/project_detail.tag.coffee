self = this
self.message = "Projects"
self.project = undefined

self.on 'mount', ->
  return

@load_project = (project) ->
  $('project-detail').show()
  $('project-list').hide()
  self.project = project
  self.update()

self.project_list = () ->
  riot.route('project/list')
  RiotControl.trigger 'load_project_list'

RiotControl.on 'load_project_detail', (project) ->
  console.log project
  self.load_project project


RiotControl.on 'load_project_list', () ->
  $('project-list').show()
  $('project-detail').hide()
