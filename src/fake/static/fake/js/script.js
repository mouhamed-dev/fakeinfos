
$(document).ready(function () {


    function formatCountry(country) {
        if (!country.id) return country.text;
        let code = country.id.toLowerCase();
        let flagUrl = `https://flagcdn.com/24x18/${code}.png`;
        return $(`
                <span style="display:flex; align-items:center; gap:8px;">
                    <img src="${flagUrl}" style="width:20px; height:15px; border-radius:2px;">
                    ${country.text}
                </span>`);
    }

    $('#pays').select2({
        templateResult: formatCountry,
        templateSelection: formatCountry,
        placeholder: 'Votre pays',
        width: "100%",
        language: { noResults: () => "Aucun résultat trouvé" }
    });
    if (!$('#pays').val()) {
        $('#pays').val('SN').trigger('change');
    }

    $('#pays').on('select2:open', function () {
        $('.select2-search__field').attr('placeholder', 'Tapez pour rechercher un pays...');
    });

    $('#genre').select2({
        placeholder: "Votre genre",
        minimumResultsForSearch: Infinity,
        width: "100%"
    });

    let currentToken = null;
    function fillIdentityData(data) {

        if (data.token) {
            currentToken = data.token;
        }

        $('#data-prenom').text(data.prenom || '-');
        $('#data-nom').text(data.nom || '-');
        $('#data-email').html(data.email ? `<u>${data.email}</u>` : '-');
        $('#data-phone').text(data.phone || '-');
        $('#data-age').text(data.age ? (data.age.toString().includes('ans') ? data.age : data.age + ' ans') : '-');
        $('#data-genre').text(data.genre || '-');
        $('#data-date_naissance').text(data.date_naissance || '-');
        $('#data-profession').text(data.profession || '-');
        $('#data-groupe_sanguin').text(data.groupe_sanguin || '-');
        $('#data-poids').text(data.poids || '-');
        $('#data-taille').text(data.taille || '-');
        $('#data-pays').text(data.pays || '-');
        $('#data-province').text(data.province || '-');
        $('#data-district').text(data.district || '-');
        $('#data-ville_commune').text(data.ville_commune || '-');
        $('#data-code_postal').text(data.code_postal || '-');
        $('#data-adresse').text(data.adresse || '-');
        $('#data-cni_recto').text(data.cni_recto || '-');
        $('#data-cni_verso').text(data.cni_verso || '-');
        $('#data-num_passport').text(data.num_passport || '-');
        $('#data-num_ninea').text(data.num_ninea || '-');
        $('#data-num_rccm').text(data.num_rccm || '-');
        $('#data-num_permis').text(data.num_permis || '-');

        $('#div-infos').fadeIn(500);
    }

    const identityScript = document.getElementById('last-identity-data');
    if (identityScript) {
        try {
            const savedData = JSON.parse(identityScript.textContent);
            if (savedData && savedData.token) {
                currentToken = savedData.token;
            }
        } catch (e) {}
    }

    let originalButtonText = $('#generateBtn').html();
    let isGenerating = false;

    $('#form').on('submit', function (e) {
        e.preventDefault();

        if (isGenerating) return;

        const pays = $('#pays').val();
        const genre = $('#genre').val();

        if (!pays || !genre) {
            alert('Veuillez sélectionner un pays et un genre');
            return;
        }

        // UI: Loader
        isGenerating = true;
        $('#generateBtn').prop('disabled', true);
        $('#generateBtn').html(`
                    <span class="flex items-center justify-center gap-2">
                        <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Génération en cours...
                    </span>
                `);

        $('#div-infos').hide();

        // REQUÊTE AJAX
        $.ajax({
            url: '/api/generate/',
            method: 'POST',
            headers: { "X-CSRFToken": "{{ csrf_token }}" },
            contentType: 'application/json',
            data: JSON.stringify({
                pays: pays,
                genre: genre
            }),
            success: function (data) {
                fillIdentityData(data);
                
                if (data.token) {
                    const newUrl = window.location.pathname + "?ref=" + data.token;
                    window.history.pushState({path: newUrl}, '', newUrl);
                }
            },
            error: function (xhr) {
                console.error("Erreur AJAX:", xhr);
                let errorMsg = 'Une erreur est survenue lors de la génération.';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                }
                alert(errorMsg);
            },
            complete: function () {
                isGenerating = false;
                $('#generateBtn').prop('disabled', false);
                $('#generateBtn').html(originalButtonText);
            }
        });
    });

    $('#downloadBtn').on('click', function (e) {
        e.preventDefault();
        
        if ($('#div-infos').is(':visible') && currentToken) {
            window.location.href = "/api/download/?ref=" + currentToken;
        } else {
            alert("Veuillez d'abord générer une identité.");
        }
    });

    $('#resetBtn').on('click', function () {
        $('#div-infos').fadeOut(500);
        $('#form')[0].reset();
        $('#pays').val(null).trigger('change');
        $('#genre').val(null).trigger('change');

        const cleanUrl = window.location.origin + window.location.pathname;
        window.history.pushState({}, document.title, cleanUrl);

        $.ajax({
            url: '/api/reset/',
            method: 'POST',
            headers: { "X-CSRFToken": "{{ csrf_token }}" },
            success: function () {
                console.log("Session nettoyée");
            }
        });
    });

});