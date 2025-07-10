document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector(".searchInput");
  const clearBtn = document.querySelector(".clear-btn");

  if (!input || !clearBtn) return

  // 입력값 변화 감지
  input.addEventListener("input", () => {
    clearBtn.style.display = input.value.trim().length > 0 ? "block" : "none";
  });

  // x 버튼 클릭 시 입력 초기화
  clearBtn.addEventListener("click", () => {
    input.value = "";
    clearBtn.style.display = "none";
    input.focus(); // UX적으로 입력창 다시 포커스
  });

  // 페이지 로드 시 query 값이 있으면 버튼 보이기
  if (input.value.trim().length > 0) {
    clearBtn.style.display = "block";
  }
});
