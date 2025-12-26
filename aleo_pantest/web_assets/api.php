<?php
/**
 * AleoPantest V3.3.0 - API Bridge
 * This file serves as a bridge for delivering data between terminal tools and the web dashboard.
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

$storage_file = 'terminal_results.json';

// Handle OPTIONS request for CORS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit;
}

// GET: Retrieve results or clear them
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (isset($_GET['clear']) && $_GET['clear'] === 'true') {
        if (file_exists($storage_file)) {
            unlink($storage_file);
        }
        echo json_encode(['status' => 'success', 'message' => 'History cleared']);
        exit;
    }

    if (file_exists($storage_file)) {
        echo file_get_contents($storage_file);
    } else {
        echo json_encode(['status' => 'empty', 'results' => []]);
    }
    exit;
}

// POST: Receive results from terminal
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);

    if (!$data) {
        http_response_code(400);
        echo json_encode(['status' => 'error', 'message' => 'Invalid JSON data']);
        exit;
    }

    // Load existing data
    $current_data = [];
    if (file_exists($storage_file)) {
        $current_data = json_decode(file_get_contents($storage_file), true);
    }

    // Add timestamp and ID
    $data['id'] = uniqid('res_');
    $data['received_at'] = date('Y-m-d H:i:s');
    
    // Append or prepend to results
    if (!isset($current_data['results'])) {
        $current_data['results'] = [];
    }
    
    array_unshift($current_data['results'], $data);
    
    // Keep only last 50 results to save space
    $current_data['results'] = array_slice($current_data['results'], 0, 50);
    $current_data['last_update'] = date('Y-m-d H:i:s');
    $current_data['status'] = 'success';

    if (file_put_contents($storage_file, json_encode($current_data, JSON_PRETTY_PRINT))) {
        echo json_encode(['status' => 'success', 'message' => 'Data received and stored', 'id' => $data['id']]);
    } else {
        http_response_code(500);
        echo json_encode(['status' => 'error', 'message' => 'Failed to save data']);
    }
    exit;
}

http_response_code(405);
echo json_encode(['status' => 'error', 'message' => 'Method not allowed']);
?>
