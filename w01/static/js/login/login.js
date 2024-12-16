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
    login_errorMessage1.style.display = 'block';
    id_input.focus(); // 첫 번째 입력 필드에 포커스 이동
    isValid = false;
  } else {
    login_errorMessage1.style.display = 'none';
  }

  // 두 번째 입력 필드 확인
  if (pw_input.value.trim() === '') {
    if (id_input.value.trim() != '') {

      login_errorMessage2.style.display = 'block';
      if (isValid) {
        pw_input.focus(); // 첫 번째 입력 필드가 비어있지 않으면 두 번째로 포커스 이동
      }
      isValid = false;
    } else {
      login_errorMessage2.style.display = 'none';
    }
  }

  // id,pw 일치시 메인화면으로 이동
  loginFrm.submit()

});

// 입력 필드에 포커스를 잃었을 때도 확인
id_input.addEventListener('blur', () => {
  if (id_input.value.trim() === '') {
    login_errorMessage1.style.display = 'block';
  } else {
    login_errorMessage1.style.display = 'none';
  }
});

pw_input.addEventListener('blur', () => {
  if (pw_input.value.trim() === '') {
    if (id_input.value.trim() != '') {

      login_errorMessage2.style.display = 'block';
    } else {
      login_errorMessage2.style.display = 'none';
    }
  }
});
