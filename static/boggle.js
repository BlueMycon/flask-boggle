"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure
  for (let row of board) {
    const $row = $(`<tr></tr>`);

      for (let letter of row) {
        const $td = $(`<td>${letter}</td>`);
        $row.append($td);
      }

    $table.append($row);
  }
}


async function handleWordInput(evt) {
  evt.preventDefault();

  const word = $wordInput.val().toUpperCase();
  console.log("word=", word);
  const response = await axios.post(
    "/api/score-word",
    { gameId, word }
  );
  const result = response.data.result;
  console.log("result=", result);

  if (result === "not-word") {
    $message.text("Not a valid word!");
  } else if (result === "not-on-board") {
    $message.text("Your word is not on the board");
  } else {
    $message.text("Score!");
    $playedWords.append($(`<li>${word}</li>`));
  }
}

$form.on("submit", handleWordInput)

start();