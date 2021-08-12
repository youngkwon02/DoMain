let isUnLocked = false;

const widgetLockToggle = () => {
  if(isUnLocked) { // isUnLocked가 True일때, 화면을 lock으로 바꿀때만 실행
    let widget = document.querySelectorAll('.widget');
    for(let i = 0; i < widget.length; i++) {
      let hiddenStr = widget[i].querySelector('input').value;
      let hiddenJSON = JSON.parse(hiddenStr);
      hiddenJSON['contents']['posX'] = widget[i].style.left;
      hiddenJSON['contents']['posY'] = widget[i].style.top;
      widget[i].querySelector('input').value = JSON.stringify(hiddenJSON);
    }
    saveHiddenData();
    location.reload();
  }

  $(".modify-btn").toggleClass("hide");
  $(".moving-btn").toggleClass("hide");
  widgets = document.querySelectorAll("widgets");
  isUnLocked = !isUnLocked;
  drag(isUnLocked);
};
