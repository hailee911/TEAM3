//로그인 페이지

// input이 비었을때 에러메세지

const loginsubmitButton = document.getElementById('login_button');
const logintextInput1 = document.getElementById('id_input');
const logintextInput2 = document.getElementById('pw_input');
const loginerrorMessage1 = document.getElementById('login_errorMessage1');
const loginerrorMessage2 = document.getElementById('login_errorMessage2');

// 버튼 클릭 시 입력 필드 확인
login_button.addEventListener('click', () => {
  let isValid = true;

  // 첫 번째 입력 필드 확인
  if (id_input.value.trim() === '') {
    loginerrorMessage1.style.display = 'block';
    id_input.focus(); // 첫 번째 입력 필드에 포커스 이동
    isValid = false;
  } else {
    loginerrorMessage1.style.display = 'none';
  }

  // 두 번째 입력 필드 확인
  if (pw_input.value.trim() === '') {
    if (id_input.value.trim() != '') {

      loginerrorMessage2.style.display = 'block';
      if (isValid) {
        pw_input.focus(); // 첫 번째 입력 필드가 비어있지 않으면 두 번째로 포커스 이동
      }
      isValid = false;
    } else {
      loginerrorMessage2.style.display = 'none';
    }
  }

  
  // 모든 조건이 충족되면 폼을 제출
  if (isValid) {
    loginFrm.submit();
  }
});

// 입력 필드에 포커스를 잃었을 때도 확인
id_input.addEventListener('blur', () => {
  if (id_input.value.trim() === '') {
    loginerrorMessage1.style.display = 'block';
  } else {
    loginerrorMessage1.style.display = 'none';
  }
});

pw_input.addEventListener('blur', () => {
  if (pw_input.value.trim() === '') {
    if (id_input.value.trim() != '') {

      loginerrorMessage2.style.display = 'block';
    } else {
      loginerrorMessage2.style.display = 'none';
    }
  }


});
document.addEventListener("DOMContentLoaded", function() {
  const loginErrorMsgElement = document.getElementById('login_errorMessage3');
  if (loginErrorMsgElement) {
      loginErrorMsgElement.style.display = 'block';  // 에러 메시지 보이게 설정
  }
});