/* JSON.JS */

(function ($) {
    var m = {
            '\b': '\\b',
            '\t': '\\t',
            '\n': '\\n',
            '\f': '\\f',
            '\r': '\\r',
            '"' : '\\"',
            '\\': '\\\\'
        },
        s = {
            'array': function (x) {
                var a = ['['], b, f, i, l = x.length, v;
                for (i = 0; i < l; i += 1) {
                    v = x[i];
                    f = s[typeof v];
                    if (f) {
                        v = f(v);
                        if (typeof v == 'string') {
                            if (b) {
                                a[a.length] = ',';
                            }
                            a[a.length] = v;
                            b = true;
                        }
                    }
                }
                a[a.length] = ']';
                return a.join('');
            },
            'boolean': function (x) {
                return String(x);
            },
            'null': function (x) {
                return "null";
            },
            'number': function (x) {
                return isFinite(x) ? String(x) : 'null';
            },
            'object': function (x) {
                if (x) {
                    if (x instanceof Array) {
                        return s.array(x);
                    }
                    var a = ['{'], b, f, i, v;
                    for (i in x) {
                        v = x[i];
                        f = s[typeof v];
                        if (f) {
                            v = f(v);
                            if (typeof v == 'string') {
                                if (b) {
                                    a[a.length] = ',';
                                }
                                a.push(s.string(i), ':', v);
                                b = true;
                            }
                        }
                    }
                    a[a.length] = '}';
                    return a.join('');
                }
                return 'null';
            },
            'string': function (x) {
                if (/["\\\x00-\x1f]/.test(x)) {
                    x = x.replace(/([\x00-\x1f\\"])/g, function(a, b) {
                        var c = m[b];
                        if (c) {
                            return c;
                        }
                        c = b.charCodeAt();
                        return '\\u00' +
                            Math.floor(c / 16).toString(16) +
                            (c % 16).toString(16);
                    });
                }
                return '"' + x + '"';
            }
        };

    $.toJSON = function(v) {
        var f = isNaN(v) ? s[typeof v] : s['number'];
        if (f) return f(v);
    };
    
    $.parseJSON = function(v, safe) {
        if (safe === undefined) safe = $.parseJSON.safe;
        if (safe && !/^("(\\.|[^"\\\n\r])*?"|[,:{}\[\]0-9.\-+Eaeflnr-u \n\r\t])+?$/.test(v))
            return undefined;
        return eval('('+v+')');
    };
    
    $.parseJSON.safe = false;

})(jQuery);

/* APP */

APP_LOADED   = 1;
APP_PREPARED = 2;
APP_STARTED  = 3;
APP_STOPPED  = 4;

/**
 * Applications manager and launcher
 * @author Derter
 * @version 0.1 alpha
 */
App = {

    /**
     * Applications hash.
     * Format: 
     * {
     *      application_name : application_object,
     *      ...
     * }
     */
    applications : {},


    /**
     * Returns application object by its name
     * @param {String} name
     */
    Get: function(name) {
        if (isdef(this.applications[name])) return this.applications[name];
        else return null;
    },


    /**
     * Loads application, verifies it, and adds it to app hash, then executes callback function
     * @param {String} app_name
     * @param {Function} callback
     */
    Load : function(app_name, callback) {

        // If application is already loaded, (throw an exception) do nothing.
        if (isdef(this.applications[app_name])) return;
        
        // Some application path is applications/some/some.application.js
        var app_path = 'applications/' + app_name + '.application.js?rnd=' + Math.random();
        
        // Let's load it
        $.getJSON(app_path, function(app_object){
            // After load, add it to hash
            App.applications[app_name] = app_object;
            // set proper state
            app_object.state = APP_LOADED;
            // and execute callback (if exists)
            if (typeof callback == 'function') 
                callback();
        });
    },
    
    
    /**
     * Prepares application before start (e.g. caches & retrieves data), then executes callback
     * @param {String} app_name
     * @param {Function} callback
     */
    Prepare : function(app_name, callback) {
        
        // If application is already prepared then do nothing;
        if (isdef(this.applications[app_name]) && this.applications[app_name].state >= APP_PREPARED) return;
        
        // Preloader actions
        function doPrepare(app_name, callback) {
            
            if (typeof callback != 'function') var callback = function() {}
            
            var app = App.applications[app_name];
            
            callback = callback.decorate(function() {
                app.onPrepare();
                
                // Publishing mediators
                for(var i=0; i<app.publish.length; i++) {
                    IM.Create(app, app.publish[i]);
                }
                // Subscribing to mediators
                for(var i=0; i<app.subscribe.length; i++) {
                    IM.Subscribe(app, app.subscribe[i][0], app.subscribe[i][1]);
                }
                arguments.callee.old.apply(this, arguments);
            });
            
            if (isdef(app.img_cache)) {
                var cacheloader = function(app, callback) { return function() {
                    app.cacheprocess = 0;
                    app.cachecount = 0;
                    var testCache = function(app, callback) { return function() {
                        if (app.cachecount == ++app.cacheprocess) {
                            delete(app.cacheprocess);
                            delete(app.cachecount);
                            app.state = APP_PREPARED;
                            callback();
                        }
                    } } (app, callback);
                    for(var i in app.img_cache) {
                        app.img_cache[i] = Cache.PutImage(app.img_cache[i], testCache);
                        app.cachecount++;
                    }
                    if (app.cachecount == 0) {
                        delete(app.cacheprocess);
                        delete(app.cachecount);
                        app.state = APP_PREPARED;
                        callback();
                    }
                } }(app, callback);
                cacheloader();
            }
            else {
                app.state = APP_PREPARED;
                //alert(app.name + ' is prepared');
                callback();
            }
        }

        // If application neither exist nor loaded let's load it;
        if (!isdef(this.applications[app_name]) || this.applications[app_name].state < APP_LOADED) {
            App.Load(app_name, function() {
                doPrepare(app_name, callback);
            });
        }
        else doPrepare(app_name, callback);
        
    },
    
    
    /**
     * Starts application
     * @param {String} app_name
     * @param {Function} callback
     */
    Start : function(app_name, callback) {
        
        // If application is already started then do nothing;
        if (isdef(this.applications[app_name]) && this.applications[app_name].state == APP_STARTED) return null;
        
        // Start actions
        function doStart(app_name, callback) {
            var app = App.applications[app_name];
            IM.ActivateApp(app);
            app.onStart();
            app.state = APP_STARTED;
            if (typeof callback == 'function') callback();
        }

        // If application isn't prepared let's prepare it;
        if (!isdef(this.applications[app_name]) || this.applications[app_name].state < APP_PREPARED) {
            App.Prepare(app_name, function() {
                doStart(app_name, callback);
            });
            return app_name;
        }
        else doStart(app_name, callback);
        
        return app_name;
        
    },
    
    
    /**
     * Stops application
     * @param {String} app_name
     * @param {Function} callback
     */
    Stop : function(app_name, callback) {
        // If application isn't started then do nothing;
        if (!isdef(this.applications[app_name]) || this.applications[app_name].state != APP_STARTED) return;
        var app = App.applications[app_name];
        app.onStop();
        IM.PauseApp(app);
        app.state = APP_STOPPED;
        if (typeof callback == 'function') callback();
        return app_name;
    },
    
    
    /**
     * Unloads application and deletes it from hash
     * @param {String} app_name
     * @param {Function} callback
     * @param {Boolean} delete_mediator
     */
    Unload : function(app_name, callback, delete_mediator) {
        // Is there anything to unload?
        if (!isdef(this.applications[app_name])) return null;
        
        function doUnload(app_name, callback) {
            
            App.applications[app_name].onUnload();
            
            // Unsubscribing from mediators
            for(var i=0; i<App.applications[app_name].subscribe.length; i++) {
                IM.Unsubscribe(App.applications[app_name], App.applications[app_name].subscribe[i][0], App.applications[app_name].subscribe[i][1]);
            }
    
            // Deleting published mediators
            // Often we won't delete published mediators because subscribers couldn't re-subscribe
            if (delete_mediator) IM.DeleteApp(App.applications[app_name]);
            
            delete(App.applications[app_name]);
            if (typeof callback == 'function') callback();          
        }
        
        // If application is started, stop it.
        if (this.applications[app_name].state == APP_STARTED) {
            this.Stop(app_name, function() {
                doUnload(app_name, callback);
            });
        }
        else {
            doUnload(app_name, callback);
        }
        
    }
    
}

/* EX */

/**
 * Some handy functions, objects and classes
 */

function isdef(value) {
    return !(value === undefined);
}

function format_date(formatDate, formatString) {
        
        var yyyy = formatDate.getFullYear();
        var yy = yyyy.toString().substring(2);
        var m = formatDate.getMonth() + 1;
        var mm = m < 10 ? "0" + m : m;
        var d = formatDate.getDate();
        var dd = d < 10 ? "0" + d : d;

        var h = formatDate.getHours();
        var hh = h < 10 ? "0" + h : h;
        var n = formatDate.getMinutes();
        var nn = n < 10 ? "0" + n : n;
        var s = formatDate.getSeconds();
        var ss = s < 10 ? "0" + s : s;

        var day = formatDate.getDay();
        var ddd = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'][day];
        var dddd = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'][day];

        var mmm = [
            'Янв',  'Фев',  'Мар', 
            'Апр',  'Май',  'Июн', 
            'Июл',  'Авг',  'Сен', 
            'Окт',  'Ноя',  'Дек'
        ][m-1];

        var mmmm = [
            'Январь',   'Февраль',  'Март', 
            'Апрель',   'Май',      'Июнь', 
            'Июль',     'Август',   'Сентябрь', 
            'Октябрь',  'Ноябрь',   'Декабрь'
        ][m-1];

        var mmmms = [
            'Января',   'Февраля',  'Марта', 
            'Апреля',   'Мая',      'Июня', 
            'Июля',     'Августа',  'Сентября', 
            'Октября',  'Ноября',   'Декабря'
        ][m-1];

        var mmmmv = [
            'Январе',   'Феврале',  'Марте', 
            'Апреле',   'Мае',      'Июне', 
            'Июле',     'Августе',  'Сентябре', 
            'Октябре',  'Ноябре',   'Декабре'
        ][m-1];

        formatString = formatString.replace(/mmmms/i, mmmms);
        formatString = formatString.replace(/mmmmv/i, mmmmv);
        formatString = formatString.replace(/mmmm/i, mmmm);
        formatString = formatString.replace(/mmm/i, mmm);
        formatString = formatString.replace(/dddd/i, dddd);
        formatString = formatString.replace(/ddd/i, ddd);
        
        formatString = formatString.replace(/yyyy/i, yyyy);
        formatString = formatString.replace(/yy/i, yy);
        formatString = formatString.replace(/mm/i, mm);
        formatString = formatString.replace(/m/i, m);
        formatString = formatString.replace(/dd/i, dd);
        formatString = formatString.replace(/d/i, d);
        formatString = formatString.replace(/hh/i, hh);
        formatString = formatString.replace(/h/i, h);
        formatString = formatString.replace(/nn/i, nn);
        formatString = formatString.replace(/n/i, n);
        formatString = formatString.replace(/ss/i, ss);
        formatString = formatString.replace(/s/i, s);

        return formatString;    
}

Date.prototype.format = function(format) {
    return format_date(this, format);
}

function clone(o) {
    if(!o || 'object' !== typeof o) {
        return o;
    }
    var c = 'function' === typeof o.pop ? [] : {};
    var p, v;
    for(p in o) {
        if(o.hasOwnProperty(p)) {
            v = o[p];
            if(v && 'object' === typeof v)
                c[p] = clone(v);
            else
                c[p] = v;
        }
    }
    return c;
}

var rus2date = function(str) {
    if (!str) return null;
    var day = str.substring(0, 2);
    var month = str.substring(3, 5);
    var year = str.substring(6, 10);
    var cdate = month+'/'+day+'/'+year+' '+str.substring(11, 19);
    return new Date(cdate);
}

Function.prototype.decorate = function(f) {
    var oldMe = this;
    var newMe = f;
    newMe.old = oldMe;
    return newMe;
}

Function.prototype.recover = function() {
    return this.old || this;
}

String.prototype.shorten = function(count, strict, hellip) {
    if (this.length <= count) 
        return this;
    else {
        var result = this.substring(0, count);
        if (!strict) {
            var words = result.split(' ');
            if (words.length > 1) words.pop();
            result = words.join(' ');
        }
        if (hellip) return result + '&hellip;';
        else return result + '...';
    }
}

/**
 * Hardware and software abstraction object and function set.
 */
HAL = {
    
    identifyAgent: function() {
        
        var ua = navigator.userAgent;
        var gecko = /Gecko\//.test(ua) ? ua.match(/; rv:\d+\.(\d+?)\.(\d)/) : 0;
        
        if (gecko) {
            Env.agent.isFF = true;
            if (gecko[1] == 9) Env.agent.isFF3 = true;
            if (gecko[1] == 8 && gecko[2] > 0) Env.agent.isFF2 = true;
        }
        else if ('\v'=='v') {
            Env.agent.isIE = true;
            if (!window.XMLHttpRequest) 
                Env.agent.isIE6 = true;
            else 
                if (
                    !document.documentMode || 
                    (document.documentMode && document.documentMode == 7)
                ) 
                Env.agent.isIE7 = true;
            else 
                Env.agent.isIE8 = true;
        }
        else if (/a/.__proto__=='//') {
            Env.agent.isSafari = true;
        }
        else if(/source/.test((/a/.toString+''))) {
            Env.agent.isChrome = true;
        }
        else if (/^function \(/.test([].sort)) {
            Env.agent.isOpera = true;
        }
        // Thanks to http://www.thespanner.co.uk/2009/01/29/detecting-browsers-javascript-hacks/
    },
    
    mapEvents: function(keycodes_map) {
        // Маппим джаваскрипт-события в HAL-события и передаем их в интерфейс
        $(window).keypress(function(event) {
            var key_code = event.keyCode;
            if (key_code == 0 && event.which) key_code = event.which;
            if (isdef(keycodes_map[key_code])) key_name = keycodes_map[key_code];
            else key_name = 'kUnknown';
            Interface.Event(event, 'keypress', { code: key_code, name: key_name });
            if(event.preventDefault) event.preventDefault();
            return false;
        });
    },
    
    setEnv: function() {
        // Setting width and height
        var setWH = function() {
            Env.windowHeight = $('#container').attr('offsetHeight'); 
            Env.windowWidth = $('#container').attr('offsetWidth');
        }
        $(window).bind("resize", setWH);
        setWH();
    },
        
    init: function() {

        // Определяем агента
        this.identifyAgent();
        
        // Подгружаем специальные инструкции для агента и выполняем их
        // if (Env.agent.isAmino140) IO.loadJSONFile('hal/init_amino_140.js');
        // else if (Env.agent.isAmino && !Env.agent.isOpera9) IO.loadJSONFile('hal/init_amino.js');
        // else if (Env.agent.isAmino) IO.loadJSONFile('hal/init_amino_9.js');
        // else IO.loadJSONFile('hal/init_ff.js');

        // Подгружаем кейкоды для агента
        // if (Env.agent.isAmino140) key_codes = IO.loadJSONFile('hal/keycodes_amino140.js');
        // else if (Env.agent.isAmino130 && Env.agent.isOpera9) key_codes = IO.loadJSONFile('hal/keycodes_amino140.js');
        // else if (Env.agent.isAmino130) key_codes = IO.loadJSONFile('hal/keycodes_amino130.js');
        // else if (Env.agent.isAmino125) key_codes = IO.loadJSONFile('hal/keycodes_amino.js');
        // else key_codes = IO.loadJSONFile('hal/keycodes_ff.js');
        key_codes = {
            '48': 'kDigit0',
            '49': 'kDigit1',
            '50': 'kDigit2',
            '51': 'kDigit3',
            '52': 'kDigit4',
            '53': 'kDigit5',
            '54': 'kDigit6',
            '55': 'kDigit7',
            '56': 'kDigit8',
            '57': 'kDigit9',
            '38': 'kUp',
            '40': 'kDown',
            '37': 'kLeft',
            '39': 'kRight',
            // '13': 'kOk',
            // '27': 'kMenu',
            // '116': 'kReload',
            // '8': 'kRed', /* Backspace */
            // '34':'kPgDown',
            // '33':'kPgUp'
        }

        // Маппим события
        this.mapEvents(key_codes);
        
        // Подключаем набор элементов интерфейса
        // IO.loadJSONFile('interface/ifc_default.js');
        // IO.loadJSONFile('interface/ifc_lists.js');
        // IO.loadJSONFile('interface/ifc_dialogs.js');
        // if (Env.agent.isAmino) IO.loadJSONFile('interface/ifc_amino.js');
        
        // IO.loadJSONFile('hal/text_global.js');
        // if (Env.agent.isAmino125) IO.loadJSONFile('hal/text_amino125.js');
        // if (Env.agent.isAmino130 || Env.agent.isAmino140) IO.loadJSONFile('hal/text_amino130.js');
        
        // Задаем переменные окружения
        this.setEnv();

        // Запускаемся
        IO.loadJSONFile('init.js');
    }
    
}

Env = {
    
    agent: {
        isIE: false,
        isIE6: false,
        isFF: false,
        isFF2: false,
        isFF3: false,
        isOpera: false,
        isOpera9: false,
        isSafari: false,
        isChrome: false
    },
    
    windowHeight: null,
    windowWidth: null
    
}

/**
 * Allows applications to publish and subscribe to events (messages).
 * Every app must have onMessage method to handle 'em.
 */
IM = {
    
    
    /**
     * Mediators collection.
     * Format:
     * {
     *      application1 : {
     *          mediator1 : {
     *              subscriber1 : subscriber_onMessage_method, ...
     *          }, ...
     *      }, ...
     * }
     */
    mediators : {},
    
    
    /**
     * Applications which allowed to receive messages
     */
    active_applications : {},
    
    
    /**
     * Creates mediator.
     * @param {Object} app
     * @param {String} name
     */
    Create : function(app, name) {
        if (isdef(this.mediators[app.name]) && !isdef(this.mediators[app.name][name])) {
            this.mediators[app.name][name] = {};
        }
        else if (!isdef(this.mediators[app.name])) {
            this.mediators[app.name] = {};
            this.mediators[app.name][name] = {};
        }
        else return;
    },
    
    
    /**
     * Deletes mediator
     * @param {Object} app
     * @param {String} name
     */
    Delete : function(app, name) {
        if (
            isdef(this.mediators[app.name]) && 
            isdef(this.mediators[app.name][name])
        ) {
            delete this.mediators[app.name][name];
        }
    },
    
    
    /**
     * Deletes all mediators for some application
     * @param {Object} app
     */
    DeleteApp : function(app) {
        if (isdef(this.mediators[app.name])) {
            delete this.mediators[app.name];
        }
    },
    
    
    /**
     * Allows application to receive messages
     * @param {Object} app
     */
    ActivateApp : function(app) {
        //if (isdef(this.mediators[app.name])) {
            this.active_applications[app.name] = true;
        //}     
    },
    
    
    /**
     * Prevent application from receiving messages
     * @param {Object} app
     */
    PauseApp : function(app) {
        if (isdef(this.active_applications[app.name])) {
            delete this.active_applications[app.name];
        }               
    },
    
    
    /**
     * Subscribes app 'subscriber_app' to mediator 'mediator_name' of app 'publisher_app_name'
     * @param {Object} subscriber_app
     * @param {String} publisher_app_name
     * @param {String} mediator_name
     */
    Subscribe: function(subscriber_app, publisher_app_name, mediator_name) {
        if (!isdef(this.mediators[publisher_app_name])) this.mediators[publisher_app_name] = {};
        if (!isdef(this.mediators[publisher_app_name][mediator_name])) this.mediators[publisher_app_name][mediator_name] = {};
        this.mediators[publisher_app_name][mediator_name][subscriber_app.name] = subscriber_app;
    },
    
    
    /**
     * Unsubscribes from mediator.
     * @param {Object} subscriber_app
     * @param {Object} publisher_app_name
     * @param {Object} mediator_name
     */
    Unsubscribe: function(subscriber_app, publisher_app_name, mediator_name) {
        if (
            isdef(this.mediators[publisher_app_name]) && 
            isdef(this.mediators[publisher_app_name][mediator_name]) && 
            isdef(this.mediators[publisher_app_name][mediator_name][subscriber_app.name])
        ) {
            delete this.mediators[publisher_app_name][mediator_name][subscriber_app.name];
        }
    },
    
    
    /**
     * Send message named 'message_name' with some data from application 'app' through mediator 'mediator_name'.
     * @param {Object} app
     * @param {String} mediator_name
     * @param {String} message_name
     * @param {Object} data
     */
    Message: function(app, mediator_name, message_name, data) {
        if (
            isdef(this.mediators[app.name]) && 
            isdef(this.mediators[app.name][mediator_name]) && 
            message_name != ''
        ) {
            var fullname = '' + app.name + ':' + mediator_name + ':' + message_name;
            for (var i in this.mediators[app.name][mediator_name]) {
                if (this.active_applications[i]) this.mediators[app.name][mediator_name][i].onMessage(fullname, data);
            }
        }
    }

}

Interface = {

    focus: $('body'),
     
    Init: function() {
        
        var blurEventDecorator = function() {
            Interface.focus = null;
            return arguments.callee.old.apply(this, arguments);
        }
        var focusEventDecorator = function() {
            if (Interface.focus) Interface.focus.trigger('blur');
            Interface.focus = $(this);
            return arguments.callee.old.apply(this, arguments);
        }
        var showEventDecorator = function() {
            $(this).trigger('show');
            return arguments.callee.old.apply(this, arguments);
        }
        var hideEventDecorator = function() {
            $(this).trigger('hide');
            return arguments.callee.old.apply(this, arguments);
        }

        // App.Start = App.Start.decorate(appStartDecorator);
        // App.Stop = App.Stop.decorate(appStopDecorator);

        $.fn.blur  = $.fn.blur.decorate(blurEventDecorator);
        $.fn.focus = $.fn.focus.decorate(focusEventDecorator);
        $.fn.show  = $.fn.show.decorate(showEventDecorator);
        $.fn.hide  = $.fn.hide.decorate(hideEventDecorator);
        
    },
    
    Event: function(evt, type, data) {
        if (this.focus == null) {
            $('body').trigger(type, data);
        }
        else {
            this.focus.trigger(type, data);
        }
    }

}

/**
 * Client-server data exchange
 */
IO = {
            
    QuerySync: function(method, params, id) {
        var query = {
            jsonrpc: '2.0',
            id: id ? id : "_",
            method: method
        }
        if (params) query.params = params;
        return IO.ajaxSync($.toJSON(query));
    },
  
    QueryRemote: function(method, params, callback, id, secure) {
        if (params instanceof Function && !callback && !id) var callback = params;
        var query = {
            jsonrpc: '2.0',
            id: id ? id : "_",
            method: method
        }
        if (params) query.params = params;
        return IO.ajaxRemote(query, callback, secure);
    },

    QueryAsync: function(method, params, callback, id) {
        if (params instanceof Function && !callback && !id) var callback = params;
        var query = {
            jsonrpc: '2.0',
            id: id ? id : '_',
            method: method
        }
        if (params) query.params = params;
        IO.ajaxAsync($.toJSON(query), callback);
    },
    
    QueryNotify: function(method, params) {
        var query = {
            jsonrpc: '2.0',
            method: method
        }
        if (params) query.params = params;
        $.ajax({
            async: true,
            type: 'POST',
            url: '/json',
            data: $.toJSON(query),
            dataType: 'json',
            processData: false
        });
    },
    
    BatchSync: function(query) {
        if (query instanceof Array) for (var i in query) query[i]['jsonrpc'] = '2.0';
        else if (query instanceof Object) query['jsonrpc'] = '2.0';
        return IO.ajaxSync($.toJSON(query));
    },

    BatchAsync: function(query, callback) {
        if (query instanceof Array) for (var i in query) query[i]['jsonrpc'] = '2.0';
        else if (query instanceof Object) query['jsonrpc'] = '2.0';
        IO.ajaxAsync($.toJSON(query), callback);
    },

    loadJSONFile: function(file) {
        var json_code = null;
        $.ajax({
            async: false,
            type: 'GET',
            url: file+'?rnd='+Math.random(),
            dataType: 'json',
            success: function(reply) {
                json_code = reply;
            }
        });
        return json_code;       
    },
  
    loadAJSONFile: function(file, callback) {
        $.ajax({
            async: true,
            type: 'GET',
            url: file+'?rnd='+Math.random(),
            dataType: 'json',
            success: callback
        });
    },

    loadHTMLFile: function(file) {
        var html_code = null;
        $.ajax({
            async: false,
            type: 'GET',
            url: file+'?rnd='+Math.random(),
            dataType: 'html',
            success: function(reply) {
                html_code = reply;
            }
        });
        return html_code;       
    },
    
    /* "Private" */
    
    ajaxSync: function(data) {
        var json_code = {
            error: {
                code: '-1',
                message: 'Response is NULL'
            }
        };
        $.ajax({
            async: false,
            type: 'POST',
            url: '/json',
            data: data,
            dataType: 'json',
            processData: false,
            success: function(reply) {
                json_code = reply;
            },
            error: function(a, b) {
                throw new Error(b);
            }
        });
        return json_code;
    },
  
    ajaxRemote: function(data, callback, secure) {
        if (!(callback instanceof Function)) var callback = new Function;
        var secure = true;
        $.ajax({
            url: secure ? 'https://' + document.location.host + '/jsonp' : 'http://' + document.location.host + '/jsonp',
            data: data,
            dataType: 'jsonp',
            jsonp: 'callback',
            success: callback
        });
    },
    
    ajaxAsync: function(data, callback) {
        if (!(callback instanceof Function)) var callback = new Function;
        $.ajax({
            async: true,
            type: 'POST',
            url: '/json',
            data: data,
            dataType: 'json',
            processData: false,
            success: callback
        });
    }
}