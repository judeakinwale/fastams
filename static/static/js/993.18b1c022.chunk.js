"use strict";(self.webpackChunkamsweb=self.webpackChunkamsweb||[]).push([[993],{2209:function(A,z,s){s.d(z,{Z:function(){return c}});var e=s(2791),n=s(184),c=function(A){var z=A.isVisible,s=void 0!==z&&z,c=A.title,i=A.content,t=A.footer,o=A.onClose,a=A.size,l=void 0===a?"md":a,r=function(A){if("Escape"===A.key)o()};return(0,e.useEffect)((function(){return document.addEventListener("keydown",r),function(){return document.removeEventListener("keydown",r)}})),s?(0,n.jsxs)("div",{className:"modal",onClick:o,children:[(0,n.jsx)("div",{className:"closeCon ".concat(l),children:(0,n.jsx)("span",{className:"modal-close",onClick:o,children:"\xd7"})}),(0,n.jsxs)("div",{className:"modal-dialog ".concat(l),onClick:function(A){return A.stopPropagation()},children:[(0,n.jsx)("div",{className:"modal-header",children:(0,n.jsx)("h3",{className:"modal-title",children:c})}),(0,n.jsx)("div",{className:"modal-body",children:(0,n.jsx)("div",{className:"modal-content",children:i})}),t&&(0,n.jsx)("div",{className:"modal-footer",children:t})]})]}):null}},5993:function(A,z,s){s.r(z),s.d(z,{default:function(){return h}});var e=s(9439),n=s(2791),c=s(7689),i=s(1087),t=s(1578),o=s(9126),a=s(7425),l=s(347),r=s(2209),B="styles_home__WZkrs",Q="styles_homeNav__Lijcz",d="styles_logo__Xm18S",E="styles_admin__NJ1UH",C="styles_title__kC6ME",m="styles_btnWrapper__knhX3",x="styles_registerLink__sN2Bn",j="styles_modalContainer__86sB-",U="styles_face__4-GL7",g=(s(2350),s(3348));s.p;var F=s(184),h=function(){var A=(0,c.s0)(),z=(0,n.useState)(!1),s=(0,e.Z)(z,2),h=s[0],u=s[1],R=(0,n.useState)(!1),I=(0,e.Z)(R,2),y=I[0],v=I[1];return(0,F.jsxs)("div",{className:B,children:[(0,F.jsxs)("nav",{className:Q,children:[(0,F.jsx)("div",{className:d,children:(0,F.jsx)("img",{src:g,alt:"logo"})}),(0,F.jsx)("div",{className:E,children:(0,F.jsxs)(i.rU,{to:l.Ot.ADMIN_LOGIN,children:[(0,F.jsx)(a.Xn2,{}),"Admin Login"]})})]}),(0,F.jsxs)("main",{children:[(0,F.jsx)("div",{className:C,children:(0,F.jsxs)("h1",{children:["Attendance",(0,F.jsx)("br",{}),"Management",(0,F.jsx)("br",{}),"System"]})}),(0,F.jsxs)("div",{className:m,children:[(0,F.jsxs)("div",{className:"btnContainer",children:[(0,F.jsx)("button",{className:"btn btnPurple",onClick:function(){u(!0),v(!0)},children:"Clock In"}),(0,F.jsx)("button",{className:"btn btnBlack",onClick:function(){u(!0),v(!1)},children:"Clock Out"})]}),(0,F.jsxs)("div",{className:x,children:["Not yet registered?",(0,F.jsx)(i.rU,{to:l.Ot.REGISTER,children:"SignUp here"})]})]})]}),(0,F.jsx)(r.Z,{isVisible:h,title:(0,F.jsxs)("div",{style:{fontSize:"18px"},children:[" ",y?"Clock In with?":"Clock Out with ?"]}),size:"md",content:(0,F.jsxs)("div",{className:j,children:[(0,F.jsxs)("div",{className:U,onClick:y?function(){A(l.Ot.CLOCK_IN)}:function(){A(l.Ot.CLOCK_OUT)},children:["Face",(0,F.jsx)(t.LBL,{})]}),(0,F.jsxs)("div",{className:U,onClick:y?function(){A(l.Ot.QR_CLOCK_IN)}:function(){A(l.Ot.QR_CLOCK_Out)},children:["QR Code ",(0,F.jsx)(o.$k$,{})]})]}),onClose:function(){u(!1),v(!1)},footer:""})]})}},2350:function(){},3348:function(A){A.exports="data:image/jpeg;base64,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"}}]);
//# sourceMappingURL=993.18b1c022.chunk.js.map