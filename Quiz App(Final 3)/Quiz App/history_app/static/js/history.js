document.addEventListener('DOMContentLoaded', () => {
    const questionContainer = document.getElementById('question');
    const answersContainer = document.getElementById('answers-container');
    const resultContainer = document.getElementById('result');
    const scoreElement = document.getElementById('score');
    const timerElement = document.getElementById('timer');
    const incorrectAnswersContainer = document.getElementById('incorrect-answers-container');
    
    let questions = [];
    let currentQuestionIndex = 0;
    let score = 0;
    let timer;
    let timeRemaining = 30;
    let incorrectAnswers = [];  // Array to store incorrect answers

    // Fetch questions from the Flask API
    async function fetchQuestions() {
        try {
            const response = await fetch('/history/api/questions');
            const data = await response.json();
            console.log('Fetched questions:', data); // Log the fetched questions

            if (data && data.length > 0) {
                questions = data;
                loadQuestion(currentQuestionIndex); // Load the first question
            } else {
                console.error('No questions available');
                questionContainer.textContent = 'No questions available. Please try again later.';
            }
        } catch (error) {
            console.error('Error loading questions:', error);
            questionContainer.textContent = 'Error loading questions. Please try again later.';
        }
    }

    // Display the current question and answers
    function loadQuestion(index) {
        if (index < questions.length) {
            const question = questions[index];
            questionContainer.textContent = question.question;

            // Clear previous answers
            answersContainer.innerHTML = '';

            // Display answer buttons
            question.answers.forEach(answer => {
                const button = document.createElement('button');
                button.textContent = answer;
                button.addEventListener('click', () => checkAnswer(answer));
                answersContainer.appendChild(button);
            });

            // Reset and start the timer for the current question
            resetTimer();
            startTimer();
        }
    }

    // Check if the selected answer is correct
    function checkAnswer(selectedAnswer) {
        const correctAnswer = questions[currentQuestionIndex].correctAnswer;
        const questionText = questions[currentQuestionIndex].question;
        
        // Check if the selected answer is correct
        let feedbackMessage = '';
        if (selectedAnswer === correctAnswer) {
            score++;
            feedbackMessage = `Correct! Your score: ${score}`;
        } else {
            feedbackMessage = `Incorrect. Your score: ${score}`;
            incorrectAnswers.push({
                question: questionText,
                yourAnswer: selectedAnswer,
                correctAnswer: correctAnswer
            });  // Save the incorrect answer
        }

        // Display feedback message after answering
        const feedbackElement = document.createElement('div');
        feedbackElement.textContent = feedbackMessage;
        feedbackElement.style.fontSize = '1.2em';
        feedbackElement.style.fontWeight = 'bold';
        feedbackElement.style.marginTop = '10px';
        feedbackElement.style.color = selectedAnswer === correctAnswer ? '#388E3C' : '#D32F2F';
        
        answersContainer.appendChild(feedbackElement); // Add feedback to the answers section

        // Go to the next question after a brief delay
        setTimeout(() => {
            currentQuestionIndex++;
            if (currentQuestionIndex < questions.length) {
                loadQuestion(currentQuestionIndex);
            } else {
                endQuiz();
            }
        }, 1000); // Delay before moving to the next question (1 second)
    }

    // End the quiz and show the result
        // End the quiz and show the result
    function endQuiz() {
    clearInterval(timer);

    
    document.getElementById("question-container").classList.add("hidden");
    document.getElementById("quiz-complete").classList.remove("hidden");

    
    document.getElementById("finalScore").textContent = score;
    document.getElementById("scoreInput").value = score;

    
    displayIncorrectAnswers();
}
    // Display the list of incorrect answers
    function displayIncorrectAnswers() {
        if (incorrectAnswers.length > 0) {
            incorrectAnswersContainer.innerHTML = '<h3>Incorrect Answers:</h3>';
            const incorrectList = document.createElement('ul');
            incorrectAnswers.forEach(incorrect => {
                const listItem = document.createElement('li');
                listItem.classList.add('incorrect-answer-item');
                listItem.innerHTML = ` 
                    <p class="question">Question: ${incorrect.question}</p>
                    <p class="your-answer">Your Answer: ${incorrect.yourAnswer}</p>
                    <p class="correct-answer">Correct Answer: ${incorrect.correctAnswer}</p>
                `;
                incorrectList.appendChild(listItem);
            });
            incorrectAnswersContainer.appendChild(incorrectList);
            incorrectAnswersContainer.style.display = 'block'; // Show incorrect answers container
        } else {
            incorrectAnswersContainer.innerHTML = '<p>All answers were correct!</p>';
            incorrectAnswersContainer.style.display = 'block'; // Show that all answers were correct
        }
    }

    // Timer logic
    function startTimer() {
        timerElement.style.display = 'block'; // Show the timer
        timer = setInterval(() => {
            timeRemaining--;
            timerElement.textContent = `${timeRemaining} seconds`;

            if (timeRemaining <= 0) {
                clearInterval(timer);
                checkAnswer(null); // Automatically move to the next question
            }
        }, 1000);
    }

    function resetTimer() {
        clearInterval(timer); // Stop any existing timer
        timeRemaining = 30; // Reset timer to 30 seconds
        timerElement.textContent = `${timeRemaining} seconds`;
    }

    function restartQuiz() {
        score = 0; // Reset the score
        currentQuestionIndex = 0; // Reset the question index
        timeRemaining = 30; // Reset the timer
        timerElement.textContent = `${timeRemaining} seconds`; // Update the timer display

        // Hide the result screen and show the question container again
        resultContainer.classList.add('hidden');
        timerElement.style.display = 'block';
        incorrectAnswersContainer.style.display = 'none'; // Hide the incorrect answers section

        fetchQuestions(); // Reload the questions and restart the quiz
    }

    // Attach event listener to restart button
    const restartButton = document.getElementById('restart');
    if (restartButton) {
        restartButton.addEventListener('click', restartQuiz);
    }

    // Initialize the quiz
    fetchQuestions();
});
