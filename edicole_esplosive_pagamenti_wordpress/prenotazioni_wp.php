<?php
/**
 * Plugin Name: Simple Booking
 * Description: Sistema semplice di prenotazioni
 * Version: 1.0
 * Author: frixx + ai
 */

// Impedisce l'accesso diretto al file
if (!defined('ABSPATH')) {
    exit;
}

// Registrazione del Custom Post Type per le prenotazioni
function sb_registra_post_type_calendario() {
    $labels = array(
        'name'               => 'Prenotazioni',
        'singular_name'      => 'Prenotazione',
        'menu_name'         => 'Prenotazioni',
        'add_new'           => 'Aggiungi Nuova',
        'add_new_item'      => 'Aggiungi Nuova Prenotazione',
        'edit_item'         => 'Modifica Prenotazione',
        'view_item'         => 'Visualizza Prenotazione',
        'search_items'      => 'Cerca Prenotazioni',
    );

    $args = array(
        'labels'              => $labels,
        'public'              => true,
        'show_in_menu'       => true,
        'menu_icon'          => 'dashicons-calendar-alt',
        'supports'           => array('title'), // Supporta solo il titolo
        'has_archive'        => false,
        'publicly_queryable' => false, // Non visualizzabile pubblicamente
        'show_in_rest'       => true,  // Supporto editor Gutenberg
    );

    register_post_type('calendario', $args);
}
add_action('init', 'sb_registra_post_type_calendario');

// Aggiunge i metabox per data, ora e stato prenotazione
function sb_aggiungi_metabox() {
    add_meta_box(
        'sb_dettagli_prenotazione',           // ID univoco
        'Dettagli Prenotazione',             // Titolo del box
        'sb_render_metabox_dettagli',        // Callback function
        'calendario',                        // Post type
        'normal',                           // Posizione (normal, side, advanced)
        'high'                              // Priorità
    );
}
add_action('add_meta_boxes', 'sb_aggiungi_metabox');

// Renderizza il contenuto del metabox
function sb_render_metabox_dettagli($post) {
    // Recupera i valori salvati
    $data = get_post_meta($post->ID, '_sb_data', true);
    $ora = get_post_meta($post->ID, '_sb_ora', true);
    $stato = get_post_meta($post->ID, '_sb_stato', true);
    $nome = get_post_meta($post->ID, '_sb_nome', true);
    $email = get_post_meta($post->ID, '_sb_email', true);
    $telefono = get_post_meta($post->ID, '_sb_telefono', true);

    // Aggiunge nonce per sicurezza
    wp_nonce_field('sb_salva_dati', 'sb_nonce');
    ?>
    <div style="margin-bottom: 20px;">
        <h4 style="margin-bottom: 10px;">Dati Prenotazione</h4>
        <p>
            <label for="sb_data">Data:</label><br>
            <input type="date" id="sb_data" name="sb_data" value="<?php echo esc_attr($data); ?>">
        </p>
        <p>
            <label for="sb_ora">Ora:</label><br>
            <input type="time" id="sb_ora" name="sb_ora" value="<?php echo esc_attr($ora); ?>">
        </p>
        <p>
            <label for="sb_stato">Stato:</label><br>
            <select id="sb_stato" name="sb_stato">
                <option value="disponibile" <?php selected($stato, 'disponibile'); ?>>Disponibile</option>
                <option value="prenotato" <?php selected($stato, 'prenotato'); ?>>Prenotato</option>
                <option value="completato" <?php selected($stato, 'completato'); ?>>Completato</option>
            </select>
        </p>
    </div>

    <div style="margin-bottom: 20px;">
        <h4 style="margin-bottom: 10px;">Dati Cliente</h4>
        <p>
            <label for="sb_nome">Nome e Cognome:</label><br>
            <input type="text" id="sb_nome" name="sb_nome" value="<?php echo esc_attr($nome); ?>">
        </p>
        <p>
            <label for="sb_email">Email:</label><br>
            <input type="email" id="sb_email" name="sb_email" value="<?php echo esc_attr($email); ?>">
        </p>
        <p>
            <label for="sb_telefono">Telefono:</label><br>
            <input type="tel" id="sb_telefono" name="sb_telefono" value="<?php echo esc_attr($telefono); ?>">
        </p>
    </div>
    <?php
}

// Salva i dati del metabox
function sb_salva_metabox($post_id) {
    // Verifica il nonce per sicurezza
    if (!isset($_POST['sb_nonce']) || !wp_verify_nonce($_POST['sb_nonce'], 'sb_salva_dati')) {
        return;
    }

    // Verifica se è un salvataggio automatico
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }

    // Salva i dati
    $campi = array('data', 'ora', 'stato', 'nome', 'email', 'telefono');
    foreach ($campi as $campo) {
        if (isset($_POST['sb_' . $campo])) {
            update_post_meta(
                $post_id, 
                '_sb_' . $campo, 
                $campo === 'email' ? sanitize_email($_POST['sb_' . $campo]) : sanitize_text_field($_POST['sb_' . $campo])
            );
        }
    }
}
add_action('save_post_calendario', 'sb_salva_metabox');

// Shortcode per mostrare un calendario semplice con slot da 30 minuti, 9-13, lun-ven
// Usa la data corrente e mostra anche le settimane successive
function sb_calendario_shortcode($atts) {
    // Aggiungi nonce per sicurezza AJAX
    $nonce = wp_create_nonce('sb_prenota_nonce');
    
    // Ottieni la data corrente
    $oggi = new DateTime();
    // Numero di settimane da mostrare (puoi cambiare questo valore)
    $settimane = 2;
    // Giorni della settimana (lun-ven)
    $giorni_settimana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
    // Orari disponibili (slot da 30 minuti, 9-13)
    $orari = [];
    for ($h = 9; $h < 13; $h++) {
        $orari[] = sprintf('%02d:00', $h);
        $orari[] = sprintf('%02d:30', $h);
    }

    // CSS per il popup e il calendario
    $html = '
    <style>
        .sb-calendario { 
            max-width: 1200px; 
            margin: 0 auto; 
            font-family: Arial, sans-serif; 
            background: #fff;
            padding: 20px;
        }
        .sb-header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 20px; 
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        .sb-month-nav { 
            display: flex; 
            align-items: center; 
            gap: 20px; 
        }
        .sb-nav-btn { 
            background: none; 
            border: none; 
            font-size: 24px; 
            cursor: pointer; 
            color: #666; 
        }
        .sb-month-title { 
            font-size: 20px; 
            font-weight: bold; 
            color: #333; 
        }
        .sb-giorni-container {
            display: flex;
            gap: 10px;
        }
        .sb-giorno-column {
            flex: 1;
        }
        .sb-giorno-header {
            text-align: center;
            padding: 10px;
            font-weight: bold;
            color: #666;
            background: #f5f5f5;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .sb-giorno-data {
            text-align: center;
            padding: 5px;
            color: #333;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .sb-slots-container {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .sb-btn { 
            background-color: #4CAF50; 
            color: white; 
            padding: 8px; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer;
            width: 100%;
            font-size: 14px;
            text-align: center;
        }
        .sb-btn:hover { background-color: #45a049; }
        .sb-btn.prenotato { 
            background-color: #ff4444 !important; 
            cursor: not-allowed; 
        }
        .sb-btn.prenotato:hover { background-color: #ff4444 !important; }
        .sb-popup { display: none; position: fixed; left: 0; top: 0; width: 100%; height: 100%; 
                   background-color: rgba(0,0,0,0.5); z-index: 1000; }
        .sb-popup-content { background-color: white; margin: 15% auto; padding: 20px; 
                           border-radius: 8px; width: 90%; max-width: 500px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .sb-close { float: right; cursor: pointer; font-weight: bold; }
        .sb-form-group { margin: 15px 0; }
        .sb-form-group label { display: block; margin-bottom: 8px; color: #333; }
        .sb-form-group input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
    </style>';

    // Inizio output HTML calendario
    $html .= '<div class="sb-calendario">';
    
    // Header con navigazione mese
    $html .= '<div class="sb-header">
        <div class="sb-month-nav">
            <button class="sb-nav-btn">&lt;</button>
            <div class="sb-month-title">' . $oggi->format('F Y') . '</div>
            <button class="sb-nav-btn">&gt;</button>
        </div>
    </div>';

    // Contenitore dei giorni
    $html .= '<div class="sb-giorni-container">';

    // Ciclo sui giorni della settimana
    foreach ($giorni_settimana as $i => $giorno) {
        $data = clone $oggi;
        $data->modify($giorno . ' this week');
        
        // Se la data è nel passato, passa al prossimo giorno della settimana successiva
        if ($data < $oggi) {
            $data->modify('+1 week');
        }

        $html .= '<div class="sb-giorno-column">';
        $html .= '<div class="sb-giorno-header">' . $giorni_it[$i] . '</div>';
        $html .= '<div class="sb-giorno-data">' . $data->format('d/m') . '</div>';
        $html .= '<div class="sb-slots-container">';

        // Slot orari per questo giorno
        foreach ($orari as $ora) {
            $data_ora = $data->format('Y-m-d') . ' ' . $ora;
            
            // Controlla se lo slot è già prenotato
            $args = array(
                'post_type'  => 'calendario',
                'meta_query' => array(
                    array(
                        'key'     => '_sb_data',
                        'value'   => $data->format('Y-m-d'),
                        'compare' => '='
                    ),
                    array(
                        'key'     => '_sb_ora',
                        'value'   => $ora,
                        'compare' => '='
                    ),
                    array(
                        'key'     => '_sb_stato',
                        'value'   => 'prenotato',
                        'compare' => '='
                    )
                )
            );
            
            $query = new WP_Query($args);
            $prenotato = $query->have_posts();
            wp_reset_postdata();

            if ($prenotato) {
                $html .= '<button class="sb-btn prenotato" disabled>Prenotato</button>';
            } else {
                $html .= '<button class="sb-btn" onclick="sbMostraPopup(\'' . 
                        esc_attr($data_ora) . '\')">' . $ora . '</button>';
            }
        }

        $html .= '</div></div>'; // Chiude sb-slots-container e sb-giorno-column
    }

    $html .= '</div>'; // Chiude sb-giorni-container

    // Popup per la prenotazione
    $html .= '
    <div id="sb-popup" class="sb-popup">
        <div class="sb-popup-content">
            <span class="sb-close" onclick="sbChiudiPopup()">&times;</span>
            <h3>Prenota Appuntamento</h3>
            <form id="sb-form-prenotazione">
                <input type="hidden" id="sb-data-ora" name="data_ora">
                <input type="hidden" name="_wpnonce" value="' . $nonce . '">
                <div class="sb-form-group">
                    <label for="sb-nome">Nome e Cognome:</label>
                    <input type="text" id="sb-nome" name="nome" required>
                </div>
                <div class="sb-form-group">
                    <label for="sb-email">Email:</label>
                    <input type="email" id="sb-email" name="email" required>
                </div>
                <div class="sb-form-group">
                    <label for="sb-telefono">Telefono:</label>
                    <input type="tel" id="sb-telefono" name="telefono" required>
                </div>
                <button type="submit" class="sb-btn">Conferma Prenotazione</button>
            </form>
            <div id="sb-messaggio"></div>
        </div>
    </div>';

    // JavaScript per gestire popup e invio form
    $html .= "
    <script>
    function sbMostraPopup(dataOra) {
        document.getElementById('sb-popup').style.display = 'block';
        document.getElementById('sb-data-ora').value = dataOra;
    }

    function sbChiudiPopup() {
        document.getElementById('sb-popup').style.display = 'none';
        document.getElementById('sb-messaggio').innerHTML = '';
    }

    document.getElementById('sb-form-prenotazione').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        formData.append('action', 'sb_salva_prenotazione');

        fetch('" . admin_url('admin-ajax.php') . "', {
            method: 'POST',
            body: formData,
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('sb-messaggio').innerHTML = data.message;
            if (data.success) {
                // Aggiorna il pulsante dello slot prenotato
                const dataOra = document.getElementById('sb-data-ora').value;
                const buttons = document.querySelectorAll('.sb-btn');
                buttons.forEach(button => {
                    if (button.onclick && button.onclick.toString().includes(dataOra)) {
                        button.className = 'sb-btn prenotato';
                        button.disabled = true;
                        button.innerHTML = 'Prenotato';
                        button.onclick = null;
                    }
                });
                setTimeout(sbChiudiPopup, 2000);
                // Pulisci il form
                document.getElementById('sb-form-prenotazione').reset();
            }
        })
        .catch(error => {
            document.getElementById('sb-messaggio').innerHTML = 'Errore durante la prenotazione';
        });
    });
    </script>";

    return $html;
}
add_shortcode('sb_calendario', 'sb_calendario_shortcode');

// Gestisce la richiesta AJAX per salvare la prenotazione
function sb_salva_prenotazione() {
    check_ajax_referer('sb_prenota_nonce', '_wpnonce');

    $data_ora = sanitize_text_field($_POST['data_ora']);
    $nome = sanitize_text_field($_POST['nome']);
    $email = sanitize_email($_POST['email']);
    $telefono = sanitize_text_field($_POST['telefono']);

    // Crea una nuova prenotazione
    $post_data = array(
        'post_title'    => "Prenotazione di $nome - $data_ora",
        'post_status'   => 'publish',
        'post_type'     => 'calendario'
    );

    $post_id = wp_insert_post($post_data);

    if ($post_id) {
        update_post_meta($post_id, '_sb_data', date('Y-m-d', strtotime($data_ora)));
        update_post_meta($post_id, '_sb_ora', date('H:i', strtotime($data_ora)));
        update_post_meta($post_id, '_sb_stato', 'prenotato');
        update_post_meta($post_id, '_sb_nome', $nome);
        update_post_meta($post_id, '_sb_email', $email);
        update_post_meta($post_id, '_sb_telefono', $telefono);

        wp_send_json_success(array('message' => 'Prenotazione confermata con successo!'));
    } else {
        wp_send_json_error(array('message' => 'Errore durante la prenotazione'));
    }
}
add_action('wp_ajax_sb_salva_prenotazione', 'sb_salva_prenotazione');
add_action('wp_ajax_nopriv_sb_salva_prenotazione', 'sb_salva_prenotazione');