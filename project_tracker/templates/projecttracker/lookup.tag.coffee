self = this
self.options = []
self.results = []

self.on 'mount', ->
  return

@loadoptions = (e) ->
  lookup = $(e.target).val()
  if lookup.length > opts.minlength
    xhr = $.get("#{opts.url}?#{opts.filter}=#{lookup}")
    xhr.done () ->
      self.results = xhr.responseJSON
      self.update()
  console.log 'lookup'

@tag_selected = (e) ->
  console.log e.item.name
  console.log e.item.id
  console.log 'Item selected'
  RiotControl.trigger('tag_selected', e)
  console.log 'triggered RC'
  return false