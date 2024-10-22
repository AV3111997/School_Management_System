document.addEventListener('DOMContentLoaded', function() {
    const gradeSelect = document.querySelector('select[name="grade"]');
    const backLink = document.getElementById('back-link');
    const baseUrl = "{% url 'students-list-by-grade' '0' %}".replace('0', '');
    gradeSelect.addEventListener('change', function() {
        const gradeId = this.value;
        if (gradeId) {
            backLink.href = `${baseUrl}${gradeId}/`;
        } else {
            backLink.href = "{% url 'students-list-by-grade' 0 %}";
        }
    });
});