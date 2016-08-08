riot.route (collection, id, action) ->
  if collection == 'project' and id == 'list'
    RiotControl.trigger 'load_project_list'

riot.route.start()

