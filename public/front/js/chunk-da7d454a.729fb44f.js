(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-da7d454a"],{"0e5e":function(e,t,r){},"14c3":function(e,t,r){var n=r("c6b6"),a=r("9263");e.exports=function(e,t){var r=e.exec;if("function"===typeof r){var c=r.call(e,t);if("object"!==typeof c)throw TypeError("RegExp exec method returned something other than an Object or null");return c}if("RegExp"!==n(e))throw TypeError("RegExp#exec called on incompatible receiver");return a.call(e,t)}},5319:function(e,t,r){"use strict";var n=r("d784"),a=r("825a"),c=r("7b0b"),i=r("50c4"),o=r("a691"),u=r("1d80"),s=r("8aa5"),l=r("14c3"),f=Math.max,d=Math.min,p=Math.floor,g=/\$([$&'`]|\d\d?|<[^>]*>)/g,v=/\$([$&'`]|\d\d?)/g,m=function(e){return void 0===e?e:String(e)};n("replace",2,(function(e,t,r,n){var h=n.REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE,x=n.REPLACE_KEEPS_$0,b=h?"$":"$0";return[function(r,n){var a=u(this),c=void 0==r?void 0:r[e];return void 0!==c?c.call(r,a,n):t.call(String(a),r,n)},function(e,n){if(!h&&x||"string"===typeof n&&-1===n.indexOf(b)){var c=r(t,e,this,n);if(c.done)return c.value}var u=a(e),p=String(this),g="function"===typeof n;g||(n=String(n));var v=u.global;if(v){var R=u.unicode;u.lastIndex=0}var y=[];while(1){var S=l(u,p);if(null===S)break;if(y.push(S),!v)break;var w=String(S[0]);""===w&&(u.lastIndex=s(p,i(u.lastIndex),R))}for(var k="",I=0,$=0;$<y.length;$++){S=y[$];for(var _=String(S[0]),O=f(d(o(S.index),p.length),0),A=[],C=1;C<S.length;C++)A.push(m(S[C]));var j=S.groups;if(g){var P=[_].concat(A,O,p);void 0!==j&&P.push(j);var T=String(n.apply(void 0,P))}else T=E(_,p,O,A,j,n);O>=I&&(k+=p.slice(I,O)+T,I=O+_.length)}return k+p.slice(I)}];function E(e,r,n,a,i,o){var u=n+e.length,s=a.length,l=v;return void 0!==i&&(i=c(i),l=g),t.call(o,l,(function(t,c){var o;switch(c.charAt(0)){case"$":return"$";case"&":return e;case"`":return r.slice(0,n);case"'":return r.slice(u);case"<":o=i[c.slice(1,-1)];break;default:var l=+c;if(0===l)return t;if(l>s){var f=p(l/10);return 0===f?t:f<=s?void 0===a[f-1]?c.charAt(1):a[f-1]+c.charAt(1):t}o=a[l-1]}return void 0===o?"":o}))}}))},6547:function(e,t,r){var n=r("a691"),a=r("1d80"),c=function(e){return function(t,r){var c,i,o=String(a(t)),u=n(r),s=o.length;return u<0||u>=s?e?"":void 0:(c=o.charCodeAt(u),c<55296||c>56319||u+1===s||(i=o.charCodeAt(u+1))<56320||i>57343?e?o.charAt(u):c:e?o.slice(u,u+2):i-56320+(c-55296<<10)+65536)}};e.exports={codeAt:c(!1),charAt:c(!0)}},"6bbd":function(e,t,r){"use strict";var n=r("0e5e"),a=r.n(n);a.a},"8aa5":function(e,t,r){"use strict";var n=r("6547").charAt;e.exports=function(e,t,r){return t+(r?n(e,t).length:1)}},9263:function(e,t,r){"use strict";var n=r("ad6d"),a=r("9f7f"),c=RegExp.prototype.exec,i=String.prototype.replace,o=c,u=function(){var e=/a/,t=/b*/g;return c.call(e,"a"),c.call(t,"a"),0!==e.lastIndex||0!==t.lastIndex}(),s=a.UNSUPPORTED_Y||a.BROKEN_CARET,l=void 0!==/()??/.exec("")[1],f=u||l||s;f&&(o=function(e){var t,r,a,o,f=this,d=s&&f.sticky,p=n.call(f),g=f.source,v=0,m=e;return d&&(p=p.replace("y",""),-1===p.indexOf("g")&&(p+="g"),m=String(e).slice(f.lastIndex),f.lastIndex>0&&(!f.multiline||f.multiline&&"\n"!==e[f.lastIndex-1])&&(g="(?: "+g+")",m=" "+m,v++),r=new RegExp("^(?:"+g+")",p)),l&&(r=new RegExp("^"+g+"$(?!\\s)",p)),u&&(t=f.lastIndex),a=c.call(d?r:f,m),d?a?(a.input=a.input.slice(v),a[0]=a[0].slice(v),a.index=f.lastIndex,f.lastIndex+=a[0].length):f.lastIndex=0:u&&a&&(f.lastIndex=f.global?a.index+a[0].length:t),l&&a&&a.length>1&&i.call(a[0],r,(function(){for(o=1;o<arguments.length-2;o++)void 0===arguments[o]&&(a[o]=void 0)})),a}),e.exports=o},"9f7f":function(e,t,r){"use strict";var n=r("d039");function a(e,t){return RegExp(e,t)}t.UNSUPPORTED_Y=n((function(){var e=a("a","y");return e.lastIndex=2,null!=e.exec("abcd")})),t.BROKEN_CARET=n((function(){var e=a("^r","gy");return e.lastIndex=2,null!=e.exec("str")}))},ac1f:function(e,t,r){"use strict";var n=r("23e7"),a=r("9263");n({target:"RegExp",proto:!0,forced:/./.exec!==a},{exec:a})},d784:function(e,t,r){"use strict";r("ac1f");var n=r("6eeb"),a=r("d039"),c=r("b622"),i=r("9263"),o=r("9112"),u=c("species"),s=!a((function(){var e=/./;return e.exec=function(){var e=[];return e.groups={a:"7"},e},"7"!=="".replace(e,"$<a>")})),l=function(){return"$0"==="a".replace(/./,"$0")}(),f=c("replace"),d=function(){return!!/./[f]&&""===/./[f]("a","$0")}(),p=!a((function(){var e=/(?:)/,t=e.exec;e.exec=function(){return t.apply(this,arguments)};var r="ab".split(e);return 2!==r.length||"a"!==r[0]||"b"!==r[1]}));e.exports=function(e,t,r,f){var g=c(e),v=!a((function(){var t={};return t[g]=function(){return 7},7!=""[e](t)})),m=v&&!a((function(){var t=!1,r=/a/;return"split"===e&&(r={},r.constructor={},r.constructor[u]=function(){return r},r.flags="",r[g]=/./[g]),r.exec=function(){return t=!0,null},r[g](""),!t}));if(!v||!m||"replace"===e&&(!s||!l||d)||"split"===e&&!p){var h=/./[g],x=r(g,""[e],(function(e,t,r,n,a){return t.exec===i?v&&!a?{done:!0,value:h.call(t,r,n)}:{done:!0,value:e.call(r,t,n)}:{done:!1}}),{REPLACE_KEEPS_$0:l,REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE:d}),b=x[0],E=x[1];n(String.prototype,e,b),n(RegExp.prototype,g,2==t?function(e,t){return E.call(e,this,t)}:function(e){return E.call(e,this)})}f&&o(RegExp.prototype[g],"sham",!0)}},e876:function(e,t,r){"use strict";r.d(t,"a",(function(){return c}));r("96cf");var n=r("c964"),a=r("b775"),c=function(){var e=Object(n["a"])(regeneratorRuntime.mark((function e(t){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.abrupt("return",a["a"].get("/public/captcha",{params:{sid:t}}));case 1:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}()},ea04:function(e,t,r){"use strict";r.r(t);var n=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("div",{staticClass:"main"},[r("a-button",{staticStyle:{color:"#ee521c"},on:{click:e.valid}},[e._v("点击验证")]),r("a-divider",[e._v("失效？重新发送激活邮件")]),r("a-form-model",{ref:"form",attrs:{model:e.form,rules:e.rules}},[r("a-form-model-item",{attrs:{prop:"email"}},[r("a-input",{attrs:{placeholder:"请输入邮箱"},model:{value:e.form.email,callback:function(t){e.$set(e.form,"email",t)},expression:"form.email"}},[r("a-icon",{staticStyle:{color:"rgba(0,0,0,.25)"},attrs:{slot:"prefix",type:"mail"},slot:"prefix"})],1)],1),r("a-form-model-item",{attrs:{prop:"code"}},[r("a-input",{attrs:{placeholder:"请输入验证码"},model:{value:e.form.code,callback:function(t){e.$set(e.form,"code",t)},expression:"form.code"}},[r("a-icon",{staticStyle:{color:"rgba(0,0,0,.25)"},attrs:{slot:"prefix",type:"code"},slot:"prefix"}),r("img",{staticStyle:{"background-color":"#fffaf7",cursor:"pointer"},attrs:{slot:"suffix",src:this.captcha,alt:""},on:{click:e.getCaptcha},slot:"suffix"})],1)],1),r("a-form-model-item",{staticClass:"action"},[r("a-button",{attrs:{type:"primary","html-type":"submit",disabled:""===e.form.email||""===e.form.code},on:{click:e.resend}},[e._v("点击发送")])],1)],1)],1)])},a=[],c=(r("ac1f"),r("5319"),r("96cf"),r("c964")),i=r("ec26"),o=r("c24f"),u=r("e876"),s=r("ca00"),l={data:function(){return{token:"",form:{email:"diaohuayao@163.com",sid:localStorage.getItem("sid"),code:""},rules:{email:[{required:!0,message:"请输入邮箱",trigger:"blur"},{type:"email",message:"请输入正确邮箱",trigger:"blur"}],code:[{required:!0,message:"请输入验证码",trigger:"blur"},{len:4,message:"验证码为4位",trigger:"blur"}]},captcha:""}},methods:{valid:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,Object(o["j"])(e.token);case 2:e.$message.success("验证成功"),e.$router.replace({name:"Login"});case 4:case"end":return t.stop()}}),t)})))()},getCaptcha:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){var r,n;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return r=localStorage.getItem("sid"),t.next=3,Object(u["a"])(r);case 3:n=t.sent,e.captcha=n;case 5:case"end":return t.stop()}}),t)})))()},resend:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:e.$refs.form.validate(function(){var t=Object(c["a"])(regeneratorRuntime.mark((function t(r){var n;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:if(!r){t.next=9;break}return n=Object(s["a"])(),e.form.sid!==n&&(e.form.sid=n),t.next=5,Object(o["g"])(e.form);case 5:e.$message.success("已发送，请前往邮箱验证"),e.$router.replace({name:"Login"}),t.next=10;break;case 9:return t.abrupt("return",!1);case 10:case"end":return t.stop()}}),t)})));return function(e){return t.apply(this,arguments)}}());case 1:case"end":return t.stop()}}),t)})))()}},mounted:function(){this.token=this.$route.params.token;var e="";localStorage.getItem("sid")?e=localStorage.getItem("sid"):(e=Object(i["a"])(),localStorage.setItem("sid",e)),this.getCaptcha()}},f=l,d=(r("6bbd"),r("2877")),p=Object(d["a"])(f,n,a,!1,null,"d708117e",null);t["default"]=p.exports}}]);