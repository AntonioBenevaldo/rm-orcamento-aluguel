function atualizarCamposPorTipo() {
    const tipoImovel = document.querySelector('#tipo_imovel');
    const camposQuartosGaragem = document.querySelector('#campos-quartos-garagem');
    const camposEstudio = document.querySelector('#campos-estudio');

    if (!tipoImovel || !camposQuartosGaragem || !camposEstudio) {
        return;
    }

    const ehEstudio = tipoImovel.value === 'estudio';
    camposQuartosGaragem.classList.toggle('oculto', ehEstudio);
    camposEstudio.classList.toggle('oculto', !ehEstudio);
}

function controlarVagasEstudio() {
    const radios = document.querySelectorAll('input[name="estacionamento_estudio"]');
    const campoVagas = document.querySelector('#vagas_estudio');

    if (!radios.length || !campoVagas) {
        return;
    }

    const selecionado = document.querySelector('input[name="estacionamento_estudio"]:checked');
    const habilitar = selecionado && selecionado.value === 'sim';

    campoVagas.disabled = !habilitar;
    if (!habilitar) {
        campoVagas.value = 2;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const tipoImovel = document.querySelector('#tipo_imovel');
    const radiosEstudio = document.querySelectorAll('input[name="estacionamento_estudio"]');

    if (tipoImovel) {
        tipoImovel.addEventListener('change', atualizarCamposPorTipo);
    }

    radiosEstudio.forEach((radio) => {
        radio.addEventListener('change', controlarVagasEstudio);
    });

    atualizarCamposPorTipo();
    controlarVagasEstudio();
});
