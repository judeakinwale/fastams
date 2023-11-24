"use strict";(self.webpackChunkamsweb=self.webpackChunkamsweb||[]).push([[379],{6751:function(A,n,t){t.d(n,{b:function(){return e}});var z={baseURL:"https://impactlife.azurewebsites.net/api/v1"},e=t(1243).Z.create(z)},1379:function(A,n,t){t.r(n);var z=t(2791),e=t(3348),r=t(7689),o=t(347),s=t(2267),c=(t(2350),t(4928)),a=t(9373),i=t(184);n.default=function(){var A=(0,c.X)().data,n=(0,r.s0)(),t=(0,z.useContext)(a.V);return(0,i.jsxs)("div",{className:s.Z.home,children:[(0,i.jsx)("div",{className:s.Z.logo,children:(0,i.jsx)("img",{src:e,alt:"AMS Logo"})}),(0,i.jsx)("h1",{children:"Attendance"}),(0,i.jsx)("h1",{children:"Management"}),(0,i.jsx)("h1",{children:"System"}),(0,i.jsxs)("div",{style:{marginTop:"4rem"},className:"btnContainer",children:["ClockedIn"===(null===A||void 0===A?void 0:A.status)?(0,i.jsx)("div",{children:(0,i.jsx)("button",{className:"btn btnYellow",onClick:function(){n(o.oj.CLOCK_OUT)},children:"Clock Out"})}):(0,i.jsx)("div",{children:(0,i.jsx)("button",{className:"btn btnPurple",onClick:function(){n(o.oj.CLOCK_IN)},children:"Clock In"})}),(0,i.jsx)("div",{children:(0,i.jsx)("button",{className:"btn btnBlack",onClick:function(){t.logout(),n("/")},children:"Log Out"})})]})]})}},4928:function(A,n,t){t.d(n,{K:function(){return E},X:function(){return C}});var z=t(4165),e=t(5861),r=t(6751),o=t(6403),s=t(3418),c=t(2917),a=t(8096),i=t(749),u=t(5985),B=t(6414);function Q(){return(Q=(0,e.Z)((0,z.Z)().mark((function A(n){var t;return(0,z.Z)().wrap((function(A){for(;;)switch(A.prev=A.next){case 0:return A.next=2,(0,r.b)({url:"/attendance/sign-in-qr?content=".concat(n.qrCode,"&long=").concat(n.long,"&lat=").concat(n.lat),method:"POST",headers:{"Content-Type":"multipart/form-data"}});case 2:return t=A.sent,A.abrupt("return",null===t||void 0===t?void 0:t.data);case 4:case"end":return A.stop()}}),A)})))).apply(this,arguments)}function l(){return(l=(0,e.Z)((0,z.Z)().mark((function A(){var n;return(0,z.Z)().wrap((function(A){for(;;)switch(A.prev=A.next){case 0:return A.next=2,(0,r.b)({url:"/Attendance/UserAttendStatus",method:"GET",headers:{"Content-Type":"application/json",Authorization:"Bearer ".concat((0,a.KU)())}});case 2:return n=A.sent,A.abrupt("return",null===n||void 0===n?void 0:n.data);case 4:case"end":return A.stop()}}),A)})))).apply(this,arguments)}function E(){var A=(0,o.NL)(),n=(0,s.D)({mutationFn:function(A){return function(A){return Q.apply(this,arguments)}(A)},onSuccess:function(){u.Am.success("Clock in successfull",i.HK),A.invalidateQueries([B.a.clockIn])},onError:function(A){(0,i.sD)(A,i.HK)}});return{mutate:n.mutate,isError:n.isError,error:n.error,isSuccess:n.isSuccess,reset:n.reset}}function C(){var A=(0,c.a)({queryKey:[B.a.clockIn],queryFn:function(){return function(){return l.apply(this,arguments)}()},onError:function(A){u.Am.error(A,i.HK)}}),n=A.data;return void 0===n?[]:n}},2350:function(){},2267:function(A,n){n.Z={container:"styles_container__B+Po3",qrCode:"styles_qrCode__l9wVC",btnContainer:"styles_btnContainer__WZKTJ",result:"styles_result__uA2DE",logoContainer:"styles_logoContainer__UxVta",imgContainer:"styles_imgContainer__jjjBQ",home:"styles_home__3lA8v",logo:"styles_logo__LLS9j",yellow:"styles_yellow__aWFoT"}},3348:function(A){A.exports="data:image/jpeg;base64,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"}}]);
//# sourceMappingURL=379.fa611a2c.chunk.js.map