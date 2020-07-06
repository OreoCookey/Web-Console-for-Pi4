use std::io::prelude::*;
use std::net::TcpListener;
use std::net::TcpStream;
use std::fs;
use pi_status::ThreadPool;





//main loop
fn main() {

    let listener = TcpListener::bind("192.168.1.250:5000").unwrap();
    let pool = ThreadPool::new(16);

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }
}

//handling connections
fn handle_connection(mut stream: TcpStream) {

    let mut buffer = [0; 512];

    stream.read(&mut buffer).unwrap();

    //expected http request
    let get = b"GET / HTTP/1.1\r\n";
    let home = b"GET /home HTTP/1.1\r\n";
    let home2 = b"GET /home/ HTTP/1.1\r\n";
    let data = b"GET /data HTTP/1.1\r\n";
    let test = "test";

    //routing
    let (status_line, filename) = if buffer.starts_with(get) {
        ("HTTP/1.1 200 OK\r\n\r\n", "templates/index.html")

    } else if buffer.starts_with(home2){
        ("HTTP/1.1 200 OK\r\n\r\n", "templates/index.html")

    } else if buffer.starts_with(home){
        ("HTTP/1.1 200 OK\r\n\r\n", "templates/index.html")
    
    } else if buffer.starts_with(data){
        ("HTTP/1.1 200 OK\r\n\r\n", "static/data.json")
        

    //404 page   
    } else {
        ("HTTP/1.1 200 OK\r\n\r\n", "templates/404.html")
    };
    
    let contents = fs::read_to_string(filename).unwrap();
    let response = format!("{}{}", status_line, contents);

    stream.write(response.as_bytes()).unwrap();
    stream.flush().unwrap();

    println!("Request: {}", String::from_utf8_lossy(&buffer[..]));
}
