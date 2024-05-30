"use strict";

const $likeButton = $('.like-button');
const LIKES_CAFE_API = "/api/likes-cafe";

/**Makes a request to the API to see whether cafe is liked by current user
 * Returns a boolean
 */
async function isCafeLiked() {
  const cafeId = $likeButton.data('id');
  const params = new URLSearchParams({ q: cafeId });

  const response = await fetch(`${LIKES_CAFE_API}?${params}`);
  const data = await response.json();

  const liked = (data.likes === "true");
  return liked;
}

/**Given a boolean, changes inner html of button based on boolean value
*/
async function displayInitialButtonHTML(liked) {
  if (liked) {
    $likeButton.html("Unlike");
  }
  else {
    $likeButton.html("Like");
  }
}

/**Handles like button click. Makes a request to toggle like status, calls
 * function to change the display of the button
*/
async function handleLikeButtonClick() {
  const cafeId = $likeButton.data('id');

  const response = await fetch(`${LIKES_CAFE_API}-toggle`, {
    method: "POST",
    body: JSON.stringify({"cafe_id": cafeId}),
    headers: {
      "content-type": "application/json"
    }
  });
  const data = await response.json();

  if(data.liked) {
    $likeButton.html("Unlike");
  }
  else {
    $likeButton.html("Like");
  }
}

$likeButton.on("click", handleLikeButtonClick)


/**
 * On load, displays initial button html
 */
async function start() {
  const liked = await isCafeLiked();
  await displayInitialButtonHTML(liked);
}

start();

