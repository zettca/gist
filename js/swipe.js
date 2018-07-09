const root = document.querySelector('body');
const touchStart = { x: 0, y: 0 };

root.addEventListener('touchstart', handleTouchStart, false);
root.addEventListener('touchend', handleTouchEnd, false);

function handleTouchStart(e) {
  touchStart.x = e.changedTouches[0].screenX;
  touchStart.y = e.changedTouches[0].screenY;
}

function handleTouchEnd(e) {
  const dX = e.changedTouches[0].screenX - touchStart.x;
  const dY = e.changedTouches[0].screenY - touchStart.y;
  console.log(getDirection(dX, dY));
}

function getDirection(dX, dY) {
  if (dX === 0 && dY === 0) return 'TOUCH';
  if (Math.abs(dX) > Math.abs(dY)) {
    return dX > 0 ? 'RIGHT' : 'LEFT';
  } else {
    return dY > 0 ? 'DOWN' : 'UP';
  }
}
