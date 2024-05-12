const csrftoken = getCookie("csrftoken");

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("hello, world.");

  // manage the leaderboard chart
  if (document.querySelector(".guess-container") != undefined) {
    var gameId = document
      .querySelector(".guess-container")
      .getAttribute("data-game-id");

    document
      .querySelector(".submit-guess")
      .addEventListener("click", (event) => {
        event.preventDefault();

        var guessType = document.querySelector("#type").value;
        var guessText = document.querySelector("#guess").value;

        fetch(`/guess/game_id=${gameId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            guess: guessText,
            type: guessType,
          }),
        })
          .then((response) => response.json())
          .then((result) => {
            console.log(result);
            document.querySelector(".level-content").innerHTML =
              result.game_char;
            document.querySelector(".guess-message").innerHTML = result.message;
          });
      });
  }
});
