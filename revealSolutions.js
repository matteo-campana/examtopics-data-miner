/**
 * Script to automatically click all "Reveal Solution" buttons on a page
 * and "Discussion" buttons
 */

function revealAllSolutions() {
  // Find all buttons with the class "reveal-solution"
  const revealButtons = document.querySelectorAll('.btn.btn-primary.reveal-solution');
  
  console.log(`Found ${revealButtons.length} solution buttons to click.`);
  
  // Click on each button with a small delay
  revealButtons.forEach((button, index) => {
    setTimeout(() => {
      console.log(`Clicking button ${index + 1} of ${revealButtons.length}`);
      button.click();
    }, index * 300); // 300ms delay between clicks to prevent overwhelming the page
  });
}

// Function to click all discussion buttons
function clickAllDiscussionButtons() {
  // Find all discussion buttons
  const discussionButtons = document.querySelectorAll('.btn.btn-secondary.question-discussion-button');
  
  console.log(`Found ${discussionButtons.length} discussion buttons to click.`);
  
  // Click on each button with a small delay
  discussionButtons.forEach((button, index) => {
    setTimeout(() => {
      console.log(`Clicking discussion button ${index + 1} of ${discussionButtons.length}`);
      button.click();
    }, index * 300); // 300ms delay between clicks to prevent overwhelming the page
  });
}

// Execute the functions
revealAllSolutions();
clickAllDiscussionButtons();
