"use strict";(self.webpackChunkamsweb=self.webpackChunkamsweb||[]).push([[27],{4605:function(e,a,t){t.d(a,{z:function(){return n}});var n=[{title:"First Name",field:"first_name"},{title:"Last Name",field:"last_name"},{title:"Email",field:"email"}]},2453:function(e,a,t){t.r(a),t.d(a,{default:function(){return I}});var n=t(4942),r=t(1413),i=t(9439),s=t(2791),l=(t(2350),t(5088),t(5043)),o=t(4605),u=t(8424),c=t(2209),d=t(3722),m=t(5985),f=t(749),p=t(2062),v=t.n(p),x=t(347),h=t(7689),b=t(6075),g=t(643),_=t.p+"static/media/excel.7402fa8dd3dbb58dea5d.png",j=t(4045),y=t.p+"static/media/StaffTemplate.4de8ef1dd298ea6dca31.xlsx",N=t(6355),C=t(8397),S=t(184),I=function(){var e=(0,u.w4)().data,a=(0,s.useState)(!0),t=(0,i.Z)(a,2),p=t[0],I=t[1],z=(0,s.useState)(!1),Z=(0,i.Z)(z,2),w=Z[0],k=Z[1],A=(0,s.useState)({}),H=(0,i.Z)(A,2),E=H[0],F=H[1],D=(0,s.useState)(!1),q=(0,i.Z)(D,2),O=q[0],P=q[1],L=(0,s.useState)(!1),U=(0,i.Z)(L,2),T=U[0],V=U[1],B=(0,s.useState)({}),K=(0,i.Z)(B,2),M=K[0],R=K[1],Y=(0,u.WY)(),G=Y.mutate,X=Y.isSuccess,Q=Y.reset,W=(0,h.s0)(),J=(0,u._z)().data,$=(0,s.useState)(!1),ee=(0,i.Z)($,2),ae=ee[0],te=ee[1],ne=(0,s.useState)(!1),re=(0,i.Z)(ne,2),ie=re[0],se=re[1],le=(0,s.useState)([]),oe=(0,i.Z)(le,2),ue=oe[0],ce=oe[1],de=null===e||void 0===e?void 0:e.filter((function(e){return!0===e.is_admin})),me=(0,d.B)(),fe=function(e,a){F((0,r.Z)((0,r.Z)({},E),{},(0,n.Z)({},e,a)))},pe=function(e,a){R((0,r.Z)((0,r.Z)({},M),{},(0,n.Z)({},e,a)))},ve=(0,u.F_)(),xe=ve.mutate,he=ve.isError,be=ve.isSuccess,ge=ve.reset,_e=ve.error;he&&(ge(),(0,f.sD)(_e)),be&&(ge(),m.Am.success("User Deleted Successfully",f.HK));var je=(0,u.Io)(),ye=je.mutate,Ne=je.isError,Ce=je.isSuccess,Se=je.reset,Ie=je.error,ze=(0,u.Io)(),Ze=ze.mutate,we=ze.isError,ke=ze.isSuccess,Ae=ze.reset,He=ze.error;Ne&&(Se(),(0,f.sD)(Ie)),Ce&&(Se(),m.Am.success("Successful",f.HK)),we&&(Ae(),(0,f.sD)(He)),ke&&(Ae(),m.Am.success("user updated successfully",f.HK),F({}),P(!1));X&&(F({}),k(!1),Q(),m.Am.success("Admin added Successfully",f.HK));var Ee=function(){Ze(E)},Fe=function(){te(!ae),F("")},De=(0,C.p)(),qe=De.mutate,Oe=De.isSuccess,Pe=De.isError,Le=De.error,Ue=De.reset;Oe&&(Ue(),(0,f.Cq)("Uploaded Successfully"),te(!1),ce([]),V(!1)),Pe&&(Ue(),(0,f.sD)(Le));return(0,S.jsx)(b.Z,{name:"User",title:"Users",children:(0,S.jsxs)("div",{className:"report_container",children:[(0,S.jsxs)("div",{className:"button_container",children:[(0,S.jsx)("button",{className:p?"btn btnPurple":"btn",onClick:function(){I(!p)},children:"All Staffs"}),(0,S.jsx)("button",{button:!0,className:p?"btn":"btn btnPurple",onClick:function(){I(!p)},children:"Admins"}),p?null:(0,S.jsx)("button",{button:!0,className:"btn btnGreenPry",onClick:function(){k(!0)},children:"Add Admin"})]}),(0,S.jsx)("div",{className:"table_container",children:p?(0,S.jsxs)(S.Fragment,{children:[(0,S.jsxs)("div",{className:"btnContainer",children:[(0,S.jsx)("button",{type:"button",onClick:function(){V(!T),F("")},className:"btn btnSuccess",children:"Add Staff"}),(0,S.jsx)("button",{type:"button",onClick:Fe,className:"btn btnYellow",children:"Staff Bulk Upload"})]}),(0,S.jsx)(l.iA,{columns:o.z,data:e,actions:function(e){return[{name:"Attendance History",onClick:function(e){W("".concat(x.oj.ADMIN_USER_HISTORY,"/").concat(e.id))}},{name:"Edit User",onClick:function(e){F(e),P(!0)}},{name:"Delete User",onClick:function(e){v()({title:"Are you sure?",text:"Once deleted, you will not be able to recover this",icon:"warning",buttons:!0,dangerMode:!0}).then((function(a){a&&xe(e.id)}))}},{name:"Add as Admin",onClick:function(e){v()({title:"Are you sure?",text:"This user will have admin privilegde",icon:"warning",buttons:!0,dangerMode:!0}).then((function(a){if(a){var t=(0,r.Z)((0,r.Z)({},E),{},{id:e.id,is_admin:!0});ye(t)}}))}}]},selectID:"id"})]}):(0,S.jsx)(l.iA,{columns:o.z,data:de,actions:function(e){return[{name:"Remove as Admin",onClick:function(e){v()({title:"Are you sure?",text:"This user will no longer have admin privilegde",icon:"warning",buttons:!0,dangerMode:!0}).then((function(a){if(a){var t=(0,r.Z)((0,r.Z)({},E),{},{id:e.id,is_admin:!1});ye(t)}}))}}]},selectID:"id"})}),(0,S.jsx)(c.Z,{isVisible:w,title:"",size:"md",content:(0,S.jsx)("div",{className:"modal_form_container",children:(0,S.jsxs)(l.cw,{onSubmit:function(){G(E)},validation:E,errors:M,setErrors:R,className:"Form",children:[(0,S.jsx)(l.II,{name:"first_name",label:"First Name",value:E.first_name,onChange:fe,type:"text",validationHandler:pe,error:M.first_name,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,S.jsx)(l.II,{name:"last_name",label:"Last Name",value:E.last_name,onChange:fe,type:"text",validationHandler:pe,error:M.last_name,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,S.jsx)(l.II,{name:"email",label:"Email",value:E.email,onChange:fe,type:"text",validationHandler:pe,error:M.email,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,S.jsx)(l.Ph,{name:"location_id",label:"Location",value:E.location_id,onChange:fe,type:"text",validationHandler:pe,error:M.location_id,required:!0,data:J,filter:"name",filterValue:"id",size:"large",className:"formInput"}),(0,S.jsx)(l.Ph,{name:"is_on_leave",label:"Is on Leave",value:E.is_on_leave,onChange:fe,type:"checkbox",validationHandler:pe,error:M.is_on_leave,data:[{name:"True",value:!0},{name:"False",value:!1}],filter:"name",filterValue:"value",size:"large",className:"formInput"}),(0,S.jsx)(l.zx,{size:"large",type:"submit",title:me?"loading..":"Add",disabled:!!me,className:"formButton btnPurple"})]})}),onClose:function(){return k(!1)},footer:""}),(0,S.jsx)(c.Z,{isVisible:O,title:"",size:"md",content:(0,S.jsx)("div",{className:"modal_form_container",children:(0,S.jsxs)(l.cw,{onSubmit:Ee,validation:E,errors:M,setErrors:R,className:"Form",children:[(0,S.jsx)(l.II,{name:"first_name",label:"First Name",value:E.first_name,onChange:fe,type:"text",validationHandler:pe,error:M.first_name,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,S.jsx)(l.II,{name:"last_name",label:"Last Name",value:E.last_name,onChange:fe,type:"text",validationHandler:pe,error:M.last_name,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,S.jsx)(l.II,{name:"email",label:"Email",value:E.email,onChange:fe,type:"text",validationHandler:pe,error:M.email,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,S.jsx)(l.Ph,{name:"location_id",label:"Location",value:E.location_id,onChange:fe,type:"text",validationHandler:pe,error:M.location_id,required:!0,data:J,filter:"name",filterValue:"id",size:"large",className:"formInput"}),(0,S.jsx)(l.Ph,{name:"is_on_leave",label:"Is on Leave",value:E.is_on_leave,onChange:fe,type:"checkbox",validationHandler:pe,error:M.is_on_leave,data:[{name:"True",value:!0},{name:"False",value:!1}],filter:"name",filterValue:"value",size:"large",className:"formInput"}),(0,S.jsx)(l.zx,{size:"large",onClick:Ee,type:"button",title:me?"loading..":"Save",disabled:!!me,className:"formButton"})]})}),onClose:function(){P(!1),F({})},footer:""}),(0,S.jsx)(c.Z,{isVisible:T,title:"Create User Account",size:"md",content:(0,S.jsx)("div",{className:"modal_form_container",children:(0,S.jsxs)(l.cw,{onSubmit:function(){qe([E])},validation:E,errors:M,setErrors:R,className:"Form",children:[(0,S.jsx)(l.II,{name:"first_name",label:"First Name",value:E.first_name,onChange:fe,type:"text",validationHandler:pe,error:M.first_name,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,S.jsx)(l.II,{name:"last_name",label:"Last Name",value:E.last_name,onChange:fe,type:"text",validationHandler:pe,error:M.last_name,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,S.jsx)(l.II,{name:"email",label:"Email",value:E.email,onChange:fe,type:"text",validationHandler:pe,error:M.email,required:!0,readOnly:!0,size:"large",className:"formInput"}),(0,S.jsx)(l.Ph,{name:"location_id",label:"Location",value:E.location_id,onChange:fe,type:"text",validationHandler:pe,error:M.location_id,required:!0,data:J,filter:"name",filterValue:"id",size:"large",className:"formInput"}),(0,S.jsx)(l.zx,{size:"large",type:"submit",title:me?"loading..":"Add",disabled:!!me,bgColor:"btnYellow"})]})}),onClose:function(){return V(!1)},footer:""}),(0,S.jsx)(c.Z,{isVisible:ae,title:"Employee Bulk Upload",size:"md",content:(0,S.jsxs)("div",{className:"bulkModal",children:[(0,S.jsx)("h4",{children:"Download Sample File"}),(0,S.jsx)("br",{}),(0,S.jsxs)("div",{className:"downloadTemp",children:[(0,S.jsxs)("span",{children:[(0,S.jsx)("img",{src:_,alt:"Excel Icon"}),"Sample items upload"]}),(0,S.jsx)("a",{href:y,download:!0,children:"Download"})]}),(0,S.jsx)("h4",{children:"Upload .xlsx file"}),(0,S.jsx)("br",{}),ie?(0,S.jsx)(g.g4,{width:"200",color:"#c21f4a"}):(0,S.jsxs)("div",{className:"bulkUploadModal",children:[(0,S.jsx)(N.GzT,{})," ",(0,S.jsx)("h5",{children:"Select an XLSX file to upload"}),(0,S.jsx)("input",{type:"file",onChange:function(e){se(!0);var a=e.target.files[0];if("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"!==a.type)return se(!1),m.Am.error("Invalid File",f.HK);var t=new FileReader;t.onload=function(e){var a=t.result,n=j.ij(a,{type:"binary"}),r=n.SheetNames[0],i=n.Sheets[r],s=j.P6.sheet_to_json(i);if(0===s.length)return se(!1),void m.Am.error("Document is empty",f.HK);se(!1),ce(s)},t.readAsBinaryString(a)}})]}),(null===ue||void 0===ue?void 0:ue.length)>0&&(0,S.jsx)(S.Fragment,{children:(0,S.jsx)(l.Ph,{name:"location_id",label:"Location",value:E.location_id,onChange:fe,type:"text",validationHandler:pe,error:M.location_id,required:!0,data:J,filter:"name",filterValue:"id",size:"large",className:"formInput"})}),(0,S.jsxs)("div",{className:"modalBtnContainer right",children:[(0,S.jsx)(l.zx,{title:"Cancel",loading:1===me,disabled:1===me,bgColor:"btnBlack",size:"small",onClick:Fe,type:"button"}),(0,S.jsx)(l.zx,{title:"Upload",loading:1===me,disabled:1===me,bgColor:"btnYellow",size:"small",onClick:function(){for(var e=[],a=0;a<ue.length;a++)e.push((0,r.Z)({first_name:ue[a].Firstname,last_name:ue[a].Lastname,email:ue[a].Email},E));if(0===e.length)return m.Am.error("No Data to upload");qe(e)},type:"button"})]})]}),onClose:function(){return te(!1)},footer:""})]})})}},8397:function(e,a,t){t.d(a,{m:function(){return f},p:function(){return p}});var n=t(4165),r=t(5861),i=t(7689),s=t(2805),l=t(3418),o=t(6403),u=t(749),c=t(6414);function d(){return(d=(0,r.Z)((0,n.Z)().mark((function e(a){var t,r;return(0,n.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t=new FormData,Object.keys(a).forEach((function(e){t.append(e,a[e])})),e.next=4,(0,s.b)({url:"/user",method:"POST",data:t,headers:{"Content-Type":"multipart/form-data"}});case 4:return r=e.sent,e.abrupt("return",null===r||void 0===r?void 0:r.data);case 6:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function m(){return m=(0,r.Z)((0,n.Z)().mark((function e(a){var t;return(0,n.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Promise.allSettled(a.map(function(){var e=(0,r.Z)((0,n.Z)().mark((function e(a){var t;return(0,n.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,(0,s.b)({url:"/user",method:"POST",data:a,headers:{"Content-Type":"multipart/form-data"}});case 3:return t=e.sent,e.next=6,t;case 6:return e.abrupt("return",e.sent);case 9:return e.prev=9,e.t0=e.catch(0),e.abrupt("return",e.t0);case 12:case"end":return e.stop()}}),e,null,[[0,9]])})));return function(a){return e.apply(this,arguments)}}()));case 2:return t=e.sent,e.next=5,t;case 5:return e.abrupt("return",e.sent);case 6:case"end":return e.stop()}}),e)}))),m.apply(this,arguments)}function f(){(0,i.s0)();var e=(0,l.D)({mutationFn:function(e){return function(e){return d.apply(this,arguments)}(e)},onSuccess:function(){(0,u.Cq)("Registration Successful")},onError:function(e){(0,u.sD)(e)}});return{mutate:e.mutate,isError:e.isError,error:e.error,isSuccess:e.isSuccess,reset:e.reset,data:e.data}}function p(){var e=(0,o.NL)(),a=(0,l.D)({mutationFn:function(e){return function(e){return m.apply(this,arguments)}(e)},onSuccess:function(){e.invalidateQueries([c.a.user])}});return{mutate:a.mutate,isError:a.isError,error:a.error,isSuccess:a.isSuccess,reset:a.reset,data:a.data}}},5088:function(){}}]);
//# sourceMappingURL=27.69156b9a.chunk.js.map