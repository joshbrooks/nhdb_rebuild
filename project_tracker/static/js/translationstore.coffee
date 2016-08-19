window.TranslationStore = () ->

  riot.observable this
  self = this
  self.strings = {}

  self.on 'load_translations', () ->
    url = Urls['jsontag:translations']()
    request = $.get(url)
    request.done ()->
      for i in request.responseJSON
        self.strings[i.object_id] = i

  self.on 'get_trans', (translation_id) ->
    return self.strings[translation_id].translation