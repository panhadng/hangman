document.addEventListener("DOMContentLoaded", () => {
  console.log("hello socials");

  // handle the like button and its function in total
  if (document.querySelector(".like") != undefined) {
    document.querySelectorAll(".like").forEach((post) => {
      let postId = post.parentElement.parentElement
        .querySelector(".post-content")
        .getAttribute("data-post-id");
      fetch(`/like/post_id=${postId}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
      })
        .then((response) => response.json())
        .then((result) => {
          if (result === 0) {
            // if the post is not liked, make the button show "like"
            post.parentElement.parentElement.querySelector(".like").innerText =
              "Like";
          } else {
            post.parentElement.parentElement.querySelector(".like").innerText =
              "Unlike";
          }
        });

      post.addEventListener("click", () => {
        fetch(`/like/post_id=${postId}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
        })
          .then((response) => response.json())
          .then((result) => {
            if (result === 0) {
              fetch(`/like/post_id=${postId}`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": csrftoken,
                },
              }).then((response) => {
                if (response.ok) {
                  post.parentElement.parentElement.querySelector(
                    ".like"
                  ).innerText = "Unlike";
                  post.parentElement.parentElement.querySelector(
                    ".like-count"
                  ).innerText =
                    parseInt(
                      post.parentElement.parentElement.querySelector(
                        ".like-count"
                      ).innerText
                    ) + 1;
                }
              });
            } else {
              fetch(`/like/post_id=${postId}`, {
                method: "DELETE",
                headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": csrftoken,
                },
              }).then((response) => {
                if (response.ok) {
                  post.parentElement.parentElement.querySelector(
                    ".like"
                  ).innerText = "Like";
                  post.parentElement.parentElement.querySelector(
                    ".like-count"
                  ).innerText =
                    parseInt(
                      post.parentElement.parentElement.querySelector(
                        ".like-count"
                      ).innerText
                    ) - 1;
                }
              });
            }
          });
      });
    });
  }

  // handle the comment button and its functionality
  if (document.querySelector(".comment") != undefined) {
    document.querySelectorAll(".comment").forEach((post) => {
      let postId = post.parentElement.parentElement
        .querySelector(".post-content")
        .getAttribute("data-post-id");

      post.addEventListener("click", () => {
        let comment = post.parentElement.querySelector(".comment-text").value;
        if (comment.length > 0) {
          fetch(`/comment/post_id=${postId}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({
              comment: comment,
            }),
          }).then(() => {
            window.location.reload();
          });
        }
      });
    });
  }
});
