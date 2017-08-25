require.config({
    paths: {
        text: "../app/TPLinkAddonforSplunk/components/lib/text",
        'tplinkConfigTemplate' : '../app/TPLinkAddonforSplunk/components/templates/index.html'
    }
});

require([
    "underscore",
    "backbone",
    "splunkjs/mvc",
    "jquery",
    "splunkjs/mvc/simplesplunkview",
    '../app/TPLinkAddonforSplunk/components/views/settingsView',
    "text!tplinkConfigTemplate",
], function( _, Backbone, mvc, $, SimpleSplunkView, SettingsView, TPLinkConfigTemplate){

    var TPLinkConfigView = SimpleSplunkView.extend({

        className: "TPLinkConfigView",

        el: '#tplinkConfigWrapper',

        initialize: function() {
            this.options = _.extend({}, this.options);
            this.render();
        },

        _loadSettings: function() {

            var that = this;
            var configComponents = $('#tplinkConfig-template', this.$el).text();
            $("#content", this.$el).html(_.template(configComponents));

            new SettingsView({
                id: "settingsView",
                el: $('#tplinkComponentsWrapper')
            }).render();
        },

        render: function() {

            document.title = "TPLink Add-On Setup";

            var that = this;
            $(this.$el).html(_.template(TPLinkConfigTemplate));

            this._loadSettings();

            return this;
        }

    });

    new TPLinkConfigView();

});
