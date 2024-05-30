"use strict";

const $likeButton = $('.like-button');
const LIKES_RESTAURANT_API = "/api/likes-restaurant";

/**Makes a request to the API to see whether restaurant is liked by current user
 * Returns a boolean
 */
async function isRestaurantLiked() {
  const restaurantId = $likeButton.data('id');
  const params = new URLSearchParams({ q: restaurantId });

  const response = await fetch(`${LIKES_RESTAURANT_API}?${params}`);
  const data = await response.json();

  const liked = (data.likes === "true");
  return liked;
}

/**Given a boolean, changes inner HTML of button based on boolean value
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
  const restaurantId = $likeButton.data('id');

  const response = await fetch(`${LIKES_RESTAURANT_API}-toggle`, {
    method: "POST",
    body: JSON.stringify({"restaurant_id": restaurantId}),
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
  const liked = await isRestaurantLiked();
  await displayInitialButtonHTML(liked);
}

start();