"use strict";(self.webpackChunkamsweb=self.webpackChunkamsweb||[]).push([[314],{6751:function(e,n,r){r.d(n,{b:function(){return a}});var t={baseURL:"https://impactlife.azurewebsites.net/api/v1"},a=r(1243).Z.create(t)},2575:function(e,n,r){r.d(n,{f:function(){return m},p:function(){return b}});var t=r(4165),a=r(5861),i=r(6751),s=r(2791),u=r(9373),o=r(8096),c=r(3418),l=r(2917),d=r(749),f=r(6414),p=r(5985);function h(){return(h=(0,a.Z)((0,t.Z)().mark((function e(n){var r;return(0,t.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,(0,i.b)({url:"/auth",method:"POST",data:n,headers:{"Content-Type":"application/json"}});case 2:return r=e.sent,e.abrupt("return",null===r||void 0===r?void 0:r.data);case 4:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function v(){return(v=(0,a.Z)((0,t.Z)().mark((function e(){var n;return(0,t.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,(0,i.b)({url:"/auth/me",method:"GET",headers:{"Content-Type":"application/json",Authorization:"Bearer ".concat((0,o.KU)())}});case 2:return n=e.sent,e.abrupt("return",null===n||void 0===n?void 0:n.data);case 4:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function m(){var e=(0,s.useContext)(u.V),n=(0,c.D)({mutationFn:function(e){return function(e){return h.apply(this,arguments)}(e)},onSuccess:function(n){(0,d.Cq)("Login Successful"),(0,o.EV)(null===n||void 0===n?void 0:n.token),e.authenticate(null===n||void 0===n?void 0:n.token)},onError:function(e){(0,d.sD)(e)}});return{mutate:n.mutate,isError:n.isError,error:n.error,isSuccess:n.isSuccess,reset:n.reset}}function b(){var e=(0,l.a)({queryKey:[f.a.me],queryFn:function(){return function(){return v.apply(this,arguments)}()},onError:function(e){p.Am.error(e,d.HK)}}),n=e.data;return void 0===n?[]:n}},6314:function(e,n,r){r.r(n);var t=r(4942),a=r(1413),i=r(9439),s=r(2791),u=r(5043),o=r(1087),c=r(3722),l=r(2575),d=r(184);n.default=function(){var e=(0,s.useState)({}),n=(0,i.Z)(e,2),r=n[0],f=n[1],p=(0,s.useState)({}),h=(0,i.Z)(p,2),v=h[0],m=h[1],b=(0,l.f)().mutate,x=(0,c.B)(),w=function(e,n){f((0,a.Z)((0,a.Z)({},r),{},(0,t.Z)({},e,n)))},g=function(e,n){m((0,a.Z)((0,a.Z)({},v),{},(0,t.Z)({},e,n)))};return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)("h1",{children:"Login"}),(0,d.jsxs)(u.cw,{onSubmit:function(){b(r)},children:[(0,d.jsx)(u.II,{name:"email",label:"Email Address",value:r.email,onChange:w,type:"email",validationHandler:g,error:v.email,required:!0,size:"large"}),(0,d.jsx)(u.WU,{name:"password",label:"Password",value:r.password,onChange:w,validationHandler:g,error:v.password,required:!0,size:"large"}),(0,d.jsx)(u.zx,{title:"login",size:"large",className:x?"btn-disabled":"",loading:1===x,disabled:1===x})]}),(0,d.jsxs)("div",{className:"link-wrapper",children:[(0,d.jsx)("span",{children:"Don't have an Account? "}),(0,d.jsx)(o.rU,{to:"/register",children:"Enroll here"})]}),(0,d.jsxs)("div",{className:"link-wrapper",children:[(0,d.jsx)("span",{children:"Forgot your password? "}),(0,d.jsx)(o.rU,{to:"/forgot-Password",children:"Reset it here"})]})]})}},3722:function(e,n,r){r.d(n,{B:function(){return c}});var t=r(9439),a=r(2791),i=r(7413),s=r(3734),u=r(9538),o=r(6403);function c(e,n,r){var c=(0,s.cb)(e,n,r),l=(0,t.Z)(c,2),d=l[0],f=l[1],p=void 0===f?{}:f,h=(0,o.NL)({context:p.context}),v=h.getMutationCache();return(0,i.$)(a.useCallback((function(e){return v.subscribe(u.V.batchCalls(e))}),[v]),(function(){return h.isMutating(d)}),(function(){return h.isMutating(d)}))}}}]);
//# sourceMappingURL=314.7b3d6f59.chunk.js.map