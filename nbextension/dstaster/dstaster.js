define([
    'require',
    'jquery',
    'base/js/namespace',
], function (requirejs, $, Jupyter) {
    "use strict";

    // define default values for config parameters
    var params = {};

    function get_dom(cell) {
      if ('cell' in cell) {
        cell = cell.cell;
      }
      return $(cell.element);
    }

    function modify_output(cell) {
      var $cell = get_dom(cell);

      if (cell.cell_type == 'code') {
        // Hiden-code cells
        if (cell._metadata['hidden']) {
          $cell.addClass("hidden-code");

          if ($cell.find(".hidden-bar").length == 0) {
              $cell.find(".input").after(
                  '<div class="hidden-bar">'+
                  '<button>Show code</button>'+
                  '</div>'
              )
          } else {
              // Reset state
              $cell.find(".hidden-bar button").text("Show code");
          }

          var hidden = true;
          $cell.find(".hidden-bar button")
            .click(function() {
                if(hidden) {
                    $(this).parent().parent().removeClass("hidden-code");
                    $(this).text("Hide code");
                } else {
                    $(this).parent().parent().addClass("hidden-code");
                    $(this).text("Show code");
                }
                hidden = !hidden;
            });
        }
      } else if (cell.cell_type == 'markdown') {
        // .hints environment
        var $button = $('<button>Show hint</button>');
        var $targets = $cell.find('.hints li')
        $button.appendTo($targets.not('.dst-modified'))
            .each(function() {
                $(this).siblings().hide();
            })
            .click(function() {
                $(this).siblings().show();
            });

        $targets.addClass('dst-modified');
      }
    }

    var initialize = function () {
        // update params with any specified in the server's config file.
        $.extend(true, params, Jupyter.notebook.config.thisextension);

        var cells = Jupyter.notebook.get_cells();
        for(var cell of cells) {
          modify_output(cell);
        }

        // create hooks
        $([Jupyter.events]).on('rendered.MarkdownCell', function(event, target){
          modify_output(target.cell);
        });

        // add our css to the page
        $('<link/>')
            .attr({
                rel: 'stylesheet',
                type: 'text/css',
                href: requirejs.toUrl('./dstaster.css')
            })
            .appendTo('head');
    };

    // The specially-named function load_ipython_extension will be called
    // by the notebook when the nbextension is to be loaded.
    // It mustn't take too long to execute however, or the notebook will
    // assume an error has occurred.
    var load_ipython_extension = function () {
        // Once the config has been loaded, do everything else.
        // The loaded object is a javascript Promise object, so the then
        // call return immediately. See
        // https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Promise
        // for details.
        return Jupyter.notebook.config.loaded.then(initialize);
    };

    // return object to export public methods
    return {
        load_ipython_extension : load_ipython_extension
    };
});
