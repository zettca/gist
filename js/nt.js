const mkFrame = (id, url) => `<iframe src="${url}" name="${id}" width="840" height="500"></iframe>`;
const mkLink = (name) => `window.frames['${name}'].document.getElementById('troop_confirm_go').click();`;
let frames = "", links = "";
for (i=1;i<=4;i++) {
	frames += mkFrame('name'+i, window.location.href);
	links += mkLink('name'+i);
}
document.body.innerHTML = `<a href="javascript:${links}">Send Attack!</a><br>${frames}`;
