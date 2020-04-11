window.vue =new Vue({
    el: '#app',
    vuetify: new Vuetify({
      icons: {
        iconfont: 'mdi', // 'mdi' || 'mdiSvg' || 'md' || 'fa' || 'fa4' || 'faSvg'
      },          
    }),
    data:{
      mode:'macro',
      drawer: false,
      route: "",
      search:"",
      status: "OK",
      state: null,
      data: null,
      query: '',
      query_basis: '',
      message: "",
      macro_text:"",
      grids:[],
      screen_grid:{id:"-",label:"-", grid:[]},
      url_prefix: "/macro/",      
    },
    methods:{
        log_data: function (d) {
            console.log("LOG data:",d);
            this.message = d.message;
            this.status = d.status;
        },
        info: function (txt) {
            console.log("INFO:" + txt);
            this.message = txt;
            this.status = "OK";
        },
        error: function (txt, reason) {
            console.log("ERROR:" + txt, reason);
            this.message = txt;
            this.status = "ERROR";
            if (reason.hasOwnProperty("body")) {
                this.html = reason.body;
            }
        },
        exec: function (i) {
            console.log("Exec "+i);
            this.$http.get(this.url_prefix + this.screen_grid.id+"/"+i).then(function (response) {
                response.json().then(function (data) {
                    this.result = data;
                    this.log_data(data);
                }.bind(this), function (reason) { this.error("Json error ("+i+")", reason); }.bind(this));
            }.bind(this), function (reason) { this.error(""+i+" loading error", reason); }.bind(this));
        },
        load_grids: function () {
            console.log("Load grids");
            this.$http.get("/api/grid.json").then(function (response) {
                response.json().then(function (data) {
                    this.grids = data.data;
                    this.screen_grid = data.data[0];                 
                    this.log_data(data);
                }.bind(this), function (reason) { this.error("Json error ("+i+")", reason); }.bind(this));
            }.bind(this), function (reason) { this.error(""+i+" loading error", reason); }.bind(this));
        },
        save_macro_text: function(){
            console.log("Save macro definition");
            this.info("Saving macro definition");
            this.$http.post("/api/save", {data:this.macro_text}).then(function (response) {
                response.json().then(function (data) {
                    this.log_data(data);
                    this.load_grids();
                }.bind(this), function (reason) { this.error("Json error", reason); }.bind(this));
            }.bind(this), function (reason) { this.error("Save error", reason); }.bind(this));
        },
        reload_macro_text: function(){
            console.log("Reload macro definition");
            this.info("Reloading macro definition");
            this.$http.get("/api/load.yaml").then(function (response) {
                this.macro_text = response.body;
                this.info("Macro definition reloaded.")
                this.load_grids();
            }.bind(this), function (reason) { this.error("Reload error", reason); }.bind(this));
        }
    },
    computed: {
        status_color: function () {
            if (this.status == "OK") {
                return "green";
            }
            if (this.status == "ERROR") {
                return "red";
            }
            return "gray";
        },
    },
    created:function(){
        this.load_grids();
        this.reload_macro_text();
    }
  })