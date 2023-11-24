"use strict";(self.webpackChunkamsweb=self.webpackChunkamsweb||[]).push([[841],{2723:function(e,l,t){t.r(l),t.d(l,{default:function(){return _}});var n=t(7762),i=(t(2791),t(6453)),o=t(6355),r=t(9126),c=t(8225),a=t(184),d=function(e){var l=e.total,t=void 0===l?0:l,n=e.checkin,i=void 0===n?0:n,o=e.checkout,r=void 0===o?0:o,d=e.late_checkin,s=void 0===d?0:d,u=e.early_checkout,h=void 0===u?0:u,v=e.overtime_checkout,g={tooltip:{trigger:"item"},legend:{display:"flex",flexDirection:"column",width:"10%",right:"5%",marginBottom:"20px"},series:[{name:"Reports",type:"pie",radius:"95%",avoidLabelOverlap:!1,itemStyle:{borderRadius:10,borderColor:"#fff",borderWidth:2},label:{show:!0},emphasis:{label:{show:!0,fontWeight:"bold"}},labelLine:{show:!1},color:["#640ad2","#c5d86d","#d7263d"],data:[{value:t,name:"Total"},{value:i,name:"Total Check In"},{value:r,name:"Total Check Out"},{value:s,name:"Late Check Out"},{value:h,name:"Early Check Out"},{value:void 0===v?0:v,name:"Overtime Check Out"}]}]};return(0,a.jsx)(c.Z,{option:g,style:{height:"400px",width:"100%"}})},s=t(8424),u=t(6075),h="styles_activity__nyOtJ",v="styles_image__yoSlE",g="styles_textx__YkNpP",m=t(2365),f=function(e){var l=e.user,t=e.time,n=e.logout;return(0,a.jsxs)("div",{className:h,children:[(0,a.jsx)("div",{className:v,children:(0,a.jsx)("img",{src:m,alt:"icon"})}),(0,a.jsxs)("div",{className:g,children:[l," ",!0===n?"Clocked Out":"Clocked In",(0,a.jsx)("p",{children:t})]})]})},_=function(){var e=(0,s.w4)().data,l=(0,s.ip)().data,t=(0,s.XZ)().data;var c=function(e){var l,t={},i=(0,n.Z)(e);try{for(i.s();!(l=i.n()).done;){var o=l.value,r=o.email;t[r]||(t[r]=o)}}catch(c){i.e(c)}finally{i.f()}return Object.values(t)}(function(){var e=(new Date).toISOString().split("T")[0],l=[];return null===t||void 0===t||t.forEach((function(t){t.created_at.split("T")[0]===e&&l.push(t)})),l}()),h=null===c||void 0===c?void 0:c.filter((function(e){return!0===e.is_signed_in})),v=null===c||void 0===c?void 0:c.filter((function(e){return!0===e.is_signed_out})),g=null===c||void 0===c?void 0:c.filter((function(e){return!0===e.is_signed_in_late})),m=null===c||void 0===c?void 0:c.filter((function(e){return!0===e.is_signed_out_early})),_=null===c||void 0===c?void 0:c.filter((function(e){return!0===e.is_signed_out_overtime}));var x=function(e){if((null===e||void 0===e?void 0:e.length)<4)return e;var l=null===e||void 0===e?void 0:e.length;return null===e||void 0===e?void 0:e.slice(l-4,l)}(c);return console.log(x,"log"),(0,a.jsxs)(u.Z,{name:"Dashboard",title:"Dashboard",children:[(0,a.jsxs)("div",{className:"cardFlex",children:[(0,a.jsx)(i.Xg,{title:"Total Users",count:null===e||void 0===e?void 0:e.length,Icon:o.wzp,color:"cyan",colorInner:"lightCyan"}),(0,a.jsx)(i.Xg,{title:"Total Check-In",count:null!==h&&void 0!==h&&h.length?h.length:0,Icon:r.YsN,color:"gold",colorInner:"lightGold"}),(0,a.jsx)(i.Xg,{title:"Total Check-Out",count:null!==v&&void 0!==v&&v.length?v.length:0,Icon:r.Dfd,color:"crimson",colorInner:"lightCrimson"}),(0,a.jsx)(i.Xg,{title:"Late Check-In",count:null!==g&&void 0!==g&&g.length?g.length:0,Icon:r.YsN,color:"purple",colorInner:"lightPurple"}),(0,a.jsx)(i.Xg,{title:"Early Check-Out",count:null!==m&&void 0!==m&&m.length?m.length:0,Icon:r.Dfd,color:"gold",colorInner:"lightGold"}),(0,a.jsx)(i.Xg,{title:"Overtime Check-Out",count:null!==_&&void 0!==_&&_.length?_.length:0,Icon:r.Dfd,color:"crimson",colorInner:"lightCrimson"}),(0,a.jsx)(i.Xg,{title:"Absent Staff",count:null!==l&&void 0!==l&&l.length?l.length:0,Icon:o.wzp,color:"cyan",colorInner:"lightCyan"})]}),(0,a.jsxs)("div",{className:"chart",children:[(0,a.jsx)("div",{className:"chartContainer",children:(0,a.jsx)("div",{className:"chartItems",children:(0,a.jsx)(d,{total:null===e||void 0===e?void 0:e.length,latecomer:20,checkin:null!==h&&void 0!==h&&h.length?h.length:0,checkout:null!==v&&void 0!==v&&v.length?v.length:0,late_checkin:null!==g&&void 0!==g&&g.length?g.length:0,early_checkout:null!==m&&void 0!==m&&m.length?m.length:0,overtime_checkout:null!==_&&void 0!==_&&_.length?_.length:0})})}),(0,a.jsxs)("div",{className:"activityContainer",children:[(0,a.jsx)("h2",{children:"Recent Activity"}),(0,a.jsx)("div",{className:"activity",children:x.map((function(e,l){var t,n;return(0,a.jsx)(f,{user:null===(t=e.user)||void 0===t?void 0:t.last_name,time:null===(n=e.created_at)||void 0===n?void 0:n.replace("T"," at ").slice(0,-10),logout:null===e||void 0===e?void 0:e.is_signed_out})}))})]})]})]})}}}]);
//# sourceMappingURL=841.9309b7f1.chunk.js.map