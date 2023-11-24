"use strict";(self.webpackChunkamsweb=self.webpackChunkamsweb||[]).push([[87],{8593:function(e,t,n){n.d(t,{Z:function(){return s}});n(2791);var a=n(1087),i=n(347),r=n(184),s=function(e){return(0,r.jsx)("div",{className:"menubar",children:(0,r.jsxs)("ul",{children:[(0,r.jsx)("li",{className:e.time,children:(0,r.jsx)(a.rU,{to:i.oj.ADMIN_SETTINGS,children:" Time"})}),(0,r.jsx)("li",{className:e.location,children:(0,r.jsx)(a.rU,{to:i.oj.ADMIN_SETTINGS_LOCATION,children:"Location"})}),(0,r.jsx)("li",{className:e.authentication,children:(0,r.jsx)(a.rU,{to:i.oj.ADMIN_SETTINGS_AUTHENTICATION,children:"Authentication"})})]})})}},2209:function(e,t,n){n.d(t,{Z:function(){return r}});var a=n(2791),i=n(184),r=function(e){var t=e.isVisible,n=void 0!==t&&t,r=e.title,s=e.content,l=e.footer,o=e.onClose,c=e.size,d=void 0===c?"md":c,u=function(e){if("Escape"===e.key)o()};return(0,a.useEffect)((function(){return document.addEventListener("keydown",u),function(){return document.removeEventListener("keydown",u)}})),n?(0,i.jsxs)("div",{className:"modal",onClick:o,children:[(0,i.jsx)("div",{className:"closeCon ".concat(d),children:(0,i.jsx)("span",{className:"modal-close",onClick:o,children:"\xd7"})}),(0,i.jsxs)("div",{className:"modal-dialog ".concat(d),onClick:function(e){return e.stopPropagation()},children:[(0,i.jsx)("div",{className:"modal-header",children:(0,i.jsx)("h3",{className:"modal-title",children:r})}),(0,i.jsx)("div",{className:"modal-body",children:(0,i.jsx)("div",{className:"modal-content",children:s})}),l&&(0,i.jsx)("div",{className:"modal-footer",children:l})]})]}):null}},6044:function(e,t,n){n.d(t,{CP:function(){return i},rH:function(){return r},zF:function(){return a}});var a=[{title:"First Name",field:"user.first_name"},{title:"Last Name",field:"user.last_name"},{title:"Email",field:"email"},{title:"Check In Time",field:"created_at",render:function(e){return e.created_at.replace("T"," - ").slice(0,-10)}},{title:"Check Out Time",field:"updated_at",render:function(e){return e.created_at.replace("T"," - ").slice(0,-10)}}],i=[{title:"Email",field:"email"},{title:"Check In Time",field:"created_at",render:function(e){return e.created_at.replace("T"," - ").slice(0,-10)}},{title:"Check Out Time",field:"updated_at",render:function(e){return e.created_at.replace("T"," - ").slice(0,-10)}}],r=[{title:"Name",field:"name"},{title:"Address",field:"address"},{title:"Latitude",field:"latitude"},{title:"Longitude",field:"longitude"},{title:"Radius",field:"radius"}]},6725:function(e,t,n){n.r(t);var a=n(4942),i=n(1413),r=n(9439),s=n(2791),l=(n(5088),n(8820)),o=n(5763),c=n(8593),d=n(2209),u=n(5043),m=n(8424),f=n(5985),h=n(749),x=n(3722),v=n(6044),N=n(2062),j=n.n(N),g=n(6075),p=n(184);t.default=function(){var e=(0,s.useState)(!1),t=(0,r.Z)(e,2),n=t[0],N=t[1],I=(0,s.useState)(!1),C=(0,r.Z)(I,2),y=C[0],_=C[1],b=(0,s.useState)(!1),S=(0,r.Z)(b,2),Z=S[0],k=S[1],T=(0,s.useState)({}),z=(0,r.Z)(T,2),E=z[0],L=z[1],O=(0,s.useState)({}),w=(0,r.Z)(O,2),A=w[0],H=w[1],D=(0,x.B)(),q=(0,m._z)().data,U=(0,m.Qq)(),M=U.mutate,F=U.isError,G=U.isSuccess,P=U.reset,B=U.error,K=(0,m.m3)(),Q=K.mutate,R=K.isError,V=K.isSuccess,J=K.reset,W=K.error;F&&(P(),(0,h.sD)(B)),G&&(P(),N(!1),L({}),_(!1),f.Am.success("Location Updated Successfully",h.HK)),R&&(J(),(0,h.sD)(W)),V&&(L({}),N(!1),J());var X=(0,m.zz)(),Y=X.mutate,$=X.isError,ee=X.isSuccess,te=X.reset,ne=X.error;$&&(te(),(0,h.sD)(ne)),ee&&(te(),f.Am.success("Location Deleted Successfully",h.HK));var ae=function(e,t){L((0,i.Z)((0,i.Z)({},E),{},(0,a.Z)({},e,t)))},ie=function(e,t){H((0,i.Z)((0,i.Z)({},A),{},(0,a.Z)({},e,t)))};return(0,p.jsx)(g.Z,{name:"Settings",title:"Settings",children:(0,p.jsx)("div",{className:"settings_container",children:(0,p.jsx)("div",{className:"settings_container_layout",children:(0,p.jsxs)("div",{className:"setting_container",children:[(0,p.jsx)(c.Z,{location:"remote"}),(0,p.jsxs)("div",{className:"title",children:[(0,p.jsx)("span",{className:"ams__icon",children:(0,p.jsx)(o.Sw5,{})}),"Office Location",(0,p.jsx)("span",{className:"companyName",children:(0,p.jsx)(l.QML,{className:"ams__icon_btns",onClick:function(){N(!0)}})})]}),(0,p.jsx)("div",{className:"title",children:(0,p.jsx)(u.iA,{columns:v.rH,data:q,actions:function(e){return[{name:"Edit",onClick:function(e){L(e),_(!0),N(!0)}},{name:"Delete Location",onClick:function(e){j()({title:"Are you sure?",text:"Once deleted, you will not be able to recover this",icon:"warning",buttons:!0,dangerMode:!0}).then((function(t){t&&Y(e.id)}))}}]},selectID:"id",showFilter:!0})}),(0,p.jsx)(d.Z,{isVisible:n,title:"",size:"md",content:(0,p.jsx)("div",{className:"modal_form_container",children:Z?"fetching your current location":(0,p.jsxs)(u.cw,{validation:E,errors:A,setErrors:H,className:"Form",children:[(0,p.jsx)(u.II,{name:"name",label:"name",value:E.name,onChange:ae,type:"text",validationHandler:ie,error:A.name,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,p.jsx)(u.II,{name:"phone",label:"Phone",value:E.phone,onChange:ae,type:"text",validationHandler:ie,error:A.phone,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,p.jsx)(u.II,{name:"latitude",label:"Latitude",value:E.latitude,onChange:ae,type:"text",validationHandler:ie,error:A.latitude,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,p.jsx)(u.II,{name:"longitude",label:"Longitude",value:E.longitude,onChange:ae,type:"text",validationHandler:ie,error:A.longitude,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,p.jsx)(u.II,{name:"radius",label:"Radius",value:E.radius,onChange:ae,type:"text",validationHandler:ie,error:A.radius,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,p.jsx)(u.II,{name:"address",label:"address",value:E.address,onChange:ae,type:"text",validationHandler:ie,error:A.address,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,p.jsx)(u.zx,{size:"large",type:"button",onClick:function(){navigator.geolocation?(k(!0),navigator.geolocation.getCurrentPosition((function(e){L((0,i.Z)((0,i.Z)({},E),{},{longitude:e.coords.longitude.toString(),latitude:e.coords.latitude.toString()})),k(!1)}),(function(){H((0,i.Z)((0,i.Z)({},A),{},{location:"Unable to retrieve your location"}))}))):H((0,i.Z)((0,i.Z)({},A),{},{location:"Geolocation is not supported by your browser"}))},title:D?"..loading":"Use Current Location",disabled:!!D,className:"formButton"}),(0,p.jsx)(u.zx,{size:"large",onClick:function(){!0===y?M(E):Q(E)},title:D?"submitting":"Save",disabled:!!D,className:"formButton"})]})}),onClose:function(){N(!1),L({}),_(!1)},footer:""})]})})})})}},5088:function(){}}]);
//# sourceMappingURL=87.7b69b144.chunk.js.map