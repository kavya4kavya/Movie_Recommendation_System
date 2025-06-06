document.addEventListener('DOMContentLoaded', () => {
    fetchMovie();
});

function fetchMovie() {
    fetch('/get_movie')
        .then(response => response.json())
        .then(data => {
            document.getElementById('movie-poster').src = data.Poster_Link;
            document.getElementById('movie-title').innerText = data.Series_Title;
            document.getElementById('movie-overview').innerText = data.Overview;
            document.getElementById('movie-card').dataset.movieId = data.Movie_ID;
        });
}

function swipe(direction) {
    const movieId = document.getElementById('movie-card').dataset.movieId;
    fetch('/swipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ Movie_ID: movieId, swipe_direction: direction }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        fetchMovie();
    });
}
