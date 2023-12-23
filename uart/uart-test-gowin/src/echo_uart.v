// https://github.com/ben-marshall/uart/tree/master/rtl
// may need to edit 50_000_000 freq to 100_000_000 or clock speed from 100 to 50 mhz 
// to accomodate for alchitry
// adapt for gowin, remove led part

// 
// Module: impl_top
// 
// Notes:
// - Top level module to be used in an implementation.
// - To be used in conjunction with the constraints/defaults.xdc file.
// - Ports can be (un)commented depending on whether they are being used.
// - The constraints file contains a complete list of the available ports
//   including the chipkit/Arduino pins.
//

module impl_top (
    input               clk     , // Top level system clock input.
    input               rst    , // Slide switches.
    input   wire        uart_rxd, // UART Recieve pin.
    output  wire        uart_txd // UART transmit pin.
    );
    
    // Clock frequency in hertz. // gowin change clock freq https://tangnano.sipeed.com/en/examples/2_lcd.html
    // default clk freq is 27mhz https://wiki.sipeed.com/hardware/en/tang/tang-nano-20k/nano-20k.html
    parameter CLK_HZ = 270000000; // originally 50000000
    parameter BIT_RATE =   9600;
    parameter PAYLOAD_BITS = 8;
    
    wire [PAYLOAD_BITS-1:0]  uart_rx_data;
    wire        uart_rx_valid;
    wire        uart_rx_break;
    
    wire        uart_tx_busy;
    wire [PAYLOAD_BITS-1:0]  uart_tx_data;
    wire        uart_tx_en;
    
    // ------------------------------------------------------------------------- 
    
    assign uart_tx_data = uart_rx_data;
    assign uart_tx_en   = uart_rx_valid;
    
    // ------------------------------------------------------------------------- 
    
    //
    // UART RX
    uart_rx #(
    .BIT_RATE(BIT_RATE),
    .PAYLOAD_BITS(PAYLOAD_BITS),
    .CLK_HZ  (CLK_HZ  )
    ) i_uart_rx(
    .clk          (clk          ), // Top level system clock input.
    .resetn       (!rst         ), // Asynchronous active low reset.
    .uart_rxd     (uart_rxd     ), // UART Recieve pin.
    .uart_rx_en   (1'b1         ), // Recieve enable
    .uart_rx_break(uart_rx_break), // Did we get a BREAK message?
    .uart_rx_valid(uart_rx_valid), // Valid data recieved and available.
    .uart_rx_data (uart_rx_data )  // The recieved data.
    );
    
    //
    // UART Transmitter module.
    //
    uart_tx #(
    .BIT_RATE(BIT_RATE),
    .PAYLOAD_BITS(PAYLOAD_BITS),
    .CLK_HZ  (CLK_HZ  )
    ) i_uart_tx(
    .clk          (clk          ),
    .resetn       (!rst         ),
    .uart_txd     (uart_txd     ),
    .uart_tx_en   (uart_tx_en   ),
    .uart_tx_busy (uart_tx_busy ),
    .uart_tx_data (uart_tx_data ) 
    );
    
    
endmodule


// 
// Module: uart_rx 
// 
// Notes:
// - UART reciever module.
//

module uart_rx(
input  wire       clk          , // Top level system clock input.
input  wire       resetn       , // Asynchronous active low reset.
input  wire       uart_rxd     , // UART Recieve pin.
input  wire       uart_rx_en   , // Recieve enable
output wire       uart_rx_break, // Did we get a BREAK message?
output wire       uart_rx_valid, // Valid data recieved and available.
output reg  [PAYLOAD_BITS-1:0] uart_rx_data   // The recieved data.
);

// --------------------------------------------------------------------------- 
// External parameters.
// 

//
// Input bit rate of the UART line.
parameter   BIT_RATE        = 9600; // bits / sec
localparam  BIT_P           = 1_000_000_000 * 1/BIT_RATE; // nanoseconds

//
// Clock frequency in hertz.
parameter   CLK_HZ          =    50_000_000;
localparam  CLK_P           = 1_000_000_000 * 1/CLK_HZ; // nanoseconds

//
// Number of data bits recieved per UART packet.
parameter   PAYLOAD_BITS    = 8;

//
// Number of stop bits indicating the end of a packet.
parameter   STOP_BITS       = 1;

// -------------------------------------------------------------------------- 
// Internal parameters.
// 

//
// Number of clock cycles per uart bit.
localparam       CYCLES_PER_BIT     = BIT_P / CLK_P;

//
// Size of the registers which store sample counts and bit durations.
localparam       COUNT_REG_LEN      = 1+$clog2(CYCLES_PER_BIT);

// -------------------------------------------------------------------------- 
// Internal registers.
// 

//
// Internally latched value of the uart_rxd line. Helps break long timing
// paths from input pins into the logic.
reg rxd_reg;
reg rxd_reg_0;

//
// Storage for the recieved serial data.
reg [PAYLOAD_BITS-1:0] recieved_data;

//
// Counter for the number of cycles over a packet bit.
reg [COUNT_REG_LEN-1:0] cycle_counter;

//
// Counter for the number of recieved bits of the packet.
reg [3:0] bit_counter;

//
// Sample of the UART input line whenever we are in the middle of a bit frame.
reg bit_sample;

//
// Current and next states of the internal FSM.
reg [2:0] fsm_state;
reg [2:0] n_fsm_state;

localparam FSM_IDLE = 0;
localparam FSM_START= 1;
localparam FSM_RECV = 2;
localparam FSM_STOP = 3;

// --------------------------------------------------------------------------- 
// Output assignment
// 

assign uart_rx_break = uart_rx_valid && ~|recieved_data;
assign uart_rx_valid = fsm_state == FSM_STOP && n_fsm_state == FSM_IDLE;

always @(posedge clk) begin
    if(!resetn) begin
        uart_rx_data  <= {PAYLOAD_BITS{1'b0}};
    end else if (fsm_state == FSM_STOP) begin
        uart_rx_data  <= recieved_data;
    end
end

// --------------------------------------------------------------------------- 
// FSM next state selection.
// 

wire next_bit     = cycle_counter == CYCLES_PER_BIT ||
                        fsm_state       == FSM_STOP && 
                        cycle_counter   == CYCLES_PER_BIT/2;
wire payload_done = bit_counter   == PAYLOAD_BITS  ;

//
// Handle picking the next state.
always @(*) begin : p_n_fsm_state
    case(fsm_state)
        FSM_IDLE : n_fsm_state = rxd_reg      ? FSM_IDLE : FSM_START;
        FSM_START: n_fsm_state = next_bit     ? FSM_RECV : FSM_START;
        FSM_RECV : n_fsm_state = payload_done ? FSM_STOP : FSM_RECV ;
        FSM_STOP : n_fsm_state = next_bit     ? FSM_IDLE : FSM_STOP ;
        default  : n_fsm_state = FSM_IDLE;
    endcase
end

// --------------------------------------------------------------------------- 
// Internal register setting and re-setting.
// 

//
// Handle updates to the recieved data register.
integer i = 0;
always @(posedge clk) begin : p_recieved_data
    if(!resetn) begin
        recieved_data <= {PAYLOAD_BITS{1'b0}};
    end else if(fsm_state == FSM_IDLE             ) begin
        recieved_data <= {PAYLOAD_BITS{1'b0}};
    end else if(fsm_state == FSM_RECV && next_bit ) begin
        recieved_data[PAYLOAD_BITS-1] <= bit_sample;
        for ( i = PAYLOAD_BITS-2; i >= 0; i = i - 1) begin
            recieved_data[i] <= recieved_data[i+1];
        end
    end
end

//
// Increments the bit counter when recieving.
always @(posedge clk) begin : p_bit_counter
    if(!resetn) begin
        bit_counter <= 4'b0;
    end else if(fsm_state != FSM_RECV) begin
        bit_counter <= {COUNT_REG_LEN{1'b0}};
    end else if(fsm_state == FSM_RECV && next_bit) begin
        bit_counter <= bit_counter + 1'b1;
    end
end

//
// Sample the recieved bit when in the middle of a bit frame.
always @(posedge clk) begin : p_bit_sample
    if(!resetn) begin
        bit_sample <= 1'b0;
    end else if (cycle_counter == CYCLES_PER_BIT/2) begin
        bit_sample <= rxd_reg;
    end
end


//
// Increments the cycle counter when recieving.
always @(posedge clk) begin : p_cycle_counter
    if(!resetn) begin
        cycle_counter <= {COUNT_REG_LEN{1'b0}};
    end else if(next_bit) begin
        cycle_counter <= {COUNT_REG_LEN{1'b0}};
    end else if(fsm_state == FSM_START || 
                fsm_state == FSM_RECV  || 
                fsm_state == FSM_STOP   ) begin
        cycle_counter <= cycle_counter + 1'b1;
    end
end


//
// Progresses the next FSM state.
always @(posedge clk) begin : p_fsm_state
    if(!resetn) begin
        fsm_state <= FSM_IDLE;
    end else begin
        fsm_state <= n_fsm_state;
    end
end


//
// Responsible for updating the internal value of the rxd_reg.
always @(posedge clk) begin : p_rxd_reg
    if(!resetn) begin
        rxd_reg     <= 1'b1;
        rxd_reg_0   <= 1'b1;
    end else if(uart_rx_en) begin
        rxd_reg     <= rxd_reg_0;
        rxd_reg_0   <= uart_rxd;
    end
end


endmodule



// 
// Module: uart_tx 
// 
// Notes:
// - UART transmitter module.
//

module uart_tx(
input  wire         clk         , // Top level system clock input.
input  wire         resetn      , // Asynchronous active low reset.
output wire         uart_txd    , // UART transmit pin.
output wire         uart_tx_busy, // Module busy sending previous item.
input  wire         uart_tx_en  , // Send the data on uart_tx_data
input  wire [PAYLOAD_BITS-1:0]   uart_tx_data  // The data to be sent
);

// --------------------------------------------------------------------------- 
// External parameters.
// 

//
// Input bit rate of the UART line.
parameter   BIT_RATE        = 9600; // bits / sec
localparam  BIT_P           = 1_000_000_000 * 1/BIT_RATE; // nanoseconds

//
// Clock frequency in hertz.
parameter   CLK_HZ          =    50_000_000;
localparam  CLK_P           = 1_000_000_000 * 1/CLK_HZ; // nanoseconds

//
// Number of data bits recieved per UART packet.
parameter   PAYLOAD_BITS    = 8;

//
// Number of stop bits indicating the end of a packet.
parameter   STOP_BITS       = 1;

// --------------------------------------------------------------------------- 
// Internal parameters.
// 

//
// Number of clock cycles per uart bit.
localparam       CYCLES_PER_BIT     = BIT_P / CLK_P;

//
// Size of the registers which store sample counts and bit durations.
localparam       COUNT_REG_LEN      = 1+$clog2(CYCLES_PER_BIT);

// --------------------------------------------------------------------------- 
// Internal registers.
// 

//
// Internally latched value of the uart_txd line. Helps break long timing
// paths from the logic to the output pins.
reg txd_reg;

//
// Storage for the serial data to be sent.
reg [PAYLOAD_BITS-1:0] data_to_send;

//
// Counter for the number of cycles over a packet bit.
reg [COUNT_REG_LEN-1:0] cycle_counter;

//
// Counter for the number of sent bits of the packet.
reg [3:0] bit_counter;

//
// Current and next states of the internal FSM.
reg [2:0] fsm_state;
reg [2:0] n_fsm_state;

localparam FSM_IDLE = 0;
localparam FSM_START= 1;
localparam FSM_SEND = 2;
localparam FSM_STOP = 3;


// --------------------------------------------------------------------------- 
// FSM next state selection.
// 

assign uart_tx_busy = fsm_state != FSM_IDLE;
assign uart_txd     = txd_reg;

wire next_bit     = cycle_counter == CYCLES_PER_BIT;
wire payload_done = bit_counter   == PAYLOAD_BITS  ;
wire stop_done    = bit_counter   == STOP_BITS && fsm_state == FSM_STOP;

//
// Handle picking the next state.
always @(*) begin : p_n_fsm_state
    case(fsm_state)
        FSM_IDLE : n_fsm_state = uart_tx_en   ? FSM_START: FSM_IDLE ;
        FSM_START: n_fsm_state = next_bit     ? FSM_SEND : FSM_START;
        FSM_SEND : n_fsm_state = payload_done ? FSM_STOP : FSM_SEND ;
        FSM_STOP : n_fsm_state = stop_done    ? FSM_IDLE : FSM_STOP ;
        default  : n_fsm_state = FSM_IDLE;
    endcase
end

// --------------------------------------------------------------------------- 
// Internal register setting and re-setting.
// 

//
// Handle updates to the sent data register.
integer i = 0;
always @(posedge clk) begin : p_data_to_send
    if(!resetn) begin
        data_to_send <= {PAYLOAD_BITS{1'b0}};
    end else if(fsm_state == FSM_IDLE && uart_tx_en) begin
        data_to_send <= uart_tx_data;
    end else if(fsm_state       == FSM_SEND       && next_bit ) begin
        for ( i = PAYLOAD_BITS-2; i >= 0; i = i - 1) begin
            data_to_send[i] <= data_to_send[i+1];
        end
    end
end


//
// Increments the bit counter each time a new bit frame is sent.
always @(posedge clk) begin : p_bit_counter
    if(!resetn) begin
        bit_counter <= 4'b0;
    end else if(fsm_state != FSM_SEND && fsm_state != FSM_STOP) begin
        bit_counter <= {COUNT_REG_LEN{1'b0}};
    end else if(fsm_state == FSM_SEND && n_fsm_state == FSM_STOP) begin
        bit_counter <= {COUNT_REG_LEN{1'b0}};
    end else if(fsm_state == FSM_STOP&& next_bit) begin
        bit_counter <= bit_counter + 1'b1;
    end else if(fsm_state == FSM_SEND && next_bit) begin
        bit_counter <= bit_counter + 1'b1;
    end
end


//
// Increments the cycle counter when sending.
always @(posedge clk) begin : p_cycle_counter
    if(!resetn) begin
        cycle_counter <= {COUNT_REG_LEN{1'b0}};
    end else if(next_bit) begin
        cycle_counter <= {COUNT_REG_LEN{1'b0}};
    end else if(fsm_state == FSM_START || 
                fsm_state == FSM_SEND  || 
                fsm_state == FSM_STOP   ) begin
        cycle_counter <= cycle_counter + 1'b1;
    end
end


//
// Progresses the next FSM state.
always @(posedge clk) begin : p_fsm_state
    if(!resetn) begin
        fsm_state <= FSM_IDLE;
    end else begin
        fsm_state <= n_fsm_state;
    end
end


//
// Responsible for updating the internal value of the txd_reg.
always @(posedge clk) begin : p_txd_reg
    if(!resetn) begin
        txd_reg <= 1'b1;
    end else if(fsm_state == FSM_IDLE) begin
        txd_reg <= 1'b1;
    end else if(fsm_state == FSM_START) begin
        txd_reg <= 1'b0;
    end else if(fsm_state == FSM_SEND) begin
        txd_reg <= data_to_send[0];
    end else if(fsm_state == FSM_STOP) begin
        txd_reg <= 1'b1;
    end
end

endmodule
