_this = this

getWindowDimensions = ->
  w = window
  d = document
  e = d.documentElement
  g = d.getElementsByTagName('body')[0]
  x = w.innerWidth or e.clientWidth or g.clientWidth
  y = w.innerHeight or e.clientHeight or g.clientHeight
  {
    width: x
    height: y
  }

if !opts.tags
  opts.tags =
    options: []
    tags: []
if !opts.tags.options
  opts.tags.options = []
if !opts.tags.tags
  opts.tags.tags = []

handleClickOutside = (e) ->
  if !_this.root.contains(e.target)
    _this.close()
  _this.update()
  return

applyFieldText = ->
  _this.selectfield.value = ''
  i = 0
  while i < opts.tags.options.length
    item = opts.tags.options[i]
    item.selected = false
    i++
  return

@filterOptions = ->
  _this.options = opts.tags.options
  if opts.tags.filter
    _this.options = _this.options.filter((option) ->
      console.log _this.options
      attr = option[opts.tags.filter]
      attr and attr.toLowerCase().indexOf(_this.selectfield.value.toLowerCase()) > -1
    )
  _this.trigger 'filter', _this.selectfield.value
  return

@ajaxFilterOptions = (e) ->
  lookup = _this.selectfield.value.toLowerCase()
  if lookup.length > opts.minlength
    xhr = $.get("#{opts.url}?#{opts.filterfield}=#{lookup}")
    xhr.done () ->
      _this.options = xhr.responseJSON.results
      console.log _this.options
      _this.update()
      _this.trigger 'filter', _this.selectfield.value
  console.log 'lookup'

positionDropdown = ->
  w = getWindowDimensions()
  m = _this.root.querySelector('.menu')
  if !m
    return
  if !opts.tags.isvisible
    m.style.marginTop = ''
    m.style.marginLeft = ''
    return
  pos = m.getBoundingClientRect()
  if w.width < pos.left + pos.width
    m.style.marginLeft = w.width - (pos.left + pos.width) - 20 + 'px'
  if pos.left < 0
    m.style.marginLeft = '20px'
  if w.height < pos.top + pos.height
    m.style.marginTop = w.height - (pos.top + pos.height) - 20 + 'px'
  return

@navigate = (e) ->
  if [
      13
      38
      40
    ].indexOf(e.keyCode) > -1 and !opts.tags.isvisible
    e.preventDefault()
    _this.open()
    return true
  length = _this.options.length
  if length > 0 and [
      13
      38
      40
    ].indexOf(e.keyCode) > -1
    e.preventDefault()
    activeIndex = null
    i = 0
    while i < length
      item = _this.options[i]
      if item.active
        activeIndex = i
        break
      i++
    if activeIndex != null
      _this.options[activeIndex].active = false
    if e.keyCode == 38
      if activeIndex == null or activeIndex == 0
        _this.options[length - 1].active = true
      else
        _this.options[activeIndex - 1].active = true
    else if e.keyCode == 40
      if activeIndex == null or activeIndex == length - 1
        _this.options[0].active = true
      else
        _this.options[activeIndex + 1].active = true
    else if e.keyCode == 13 and activeIndex != null
      _this.select item: _this.options[activeIndex]
  true

@open = ->
  opts.tags.isvisible = true
  _this.trigger 'open'
  return

@close = ->
  if opts.tags.isvisible
    opts.tags.isvisible = false
    _this.trigger 'close'
  return

@select = (e) ->
  opts.tags.options.forEach (i) ->
    i.selected = false
  e.item.selected = true
  _this.addTag e.item
  applyFieldText()
  _this.filterOptions()
  _this.trigger 'select', e.item
  return

@addTag = (item) ->
  if opts.tags.tags.indexOf(item) == -1
    opts.tags.tags.push item
  return

@removeTag = (e) ->
  opts.tags.tags = opts.tags.tags.filter((tag) ->
    if tag._id != e.item._id
      return tag
    return
  )
  return

@on 'mount', ->
  applyFieldText()
  _this.filterOptions()
  document.addEventListener 'click', handleClickOutside
  _this.update()
  return
@on 'update', ->
  opts.tags.options.forEach (item) ->
    item._id = item._id or (Math.floor(Math.random() * 60466175) + 1679615).toString(36)
    return
  opts.tags.tags.forEach (tag) ->
    tag._id = tag._id or (Math.floor(Math.random() * 60466175) + 1679615).toString(36)
    return
  if !opts.tags.filter
    applyFieldText()
  positionDropdown()
  return
@on 'unmount', ->
  document.removeEventListener 'click', handleClickOutside
  return

# ---
# generated by js2coffee 2.2.0