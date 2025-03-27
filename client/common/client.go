package common

import (
	"bufio"
	"io"
	"net"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("log")

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID             string
	Name           string
	Surname        string
	IdNumber       string
	DateOfBirth    string
	BetNumber      string
	ServerAddress  string
	LoopAmount     int
	LoopPeriod     time.Duration
	BatchMaxAmount int
}

// Client Entity that encapsulates how
type Client struct {
	config ClientConfig
	conn   net.Conn
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig) *Client {
	client := &Client{
		config: config,
	}
	return client
}

// CreateClientSocket Initializes client socket. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func (c *Client) createClientSocket() error {
	conn, err := net.Dial("tcp", c.config.ServerAddress)
	if err != nil {
		log.Criticalf(
			"action: connect | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
	}
	c.conn = conn
	return nil
}

// StartClientLoop Send messages to the client until some time threshold is met
func (c *Client) StartClientLoop() {
	signalChannel := make(chan os.Signal, 1)
	signal.Notify(signalChannel, syscall.SIGTERM)

	// There is an autoincremental msgID to identify every message sent
	// Messages if the message amount threshold has not been surpassed
	select {
	case <-signalChannel:
		if c.conn != nil {
			c.conn.Close()
			log.Infof("action: close_client_socket | result: success")
		}
		return
	default:
		// Create the connection the server in every loop iteration. Send an
		err := c.createClientSocket()
		if err != nil {
			log.Errorf("action: create_client_socket | result: fail | client_id: %v | error: %v",
				c.config.ID,
				err,
			)
			c.conn.Close()
			return
		}

		err = c.doBets()
		if err != nil {
			log.Errorf("action: do_bet | result: fail | client_id: %v | error: %v",
				c.config.ID,
				err,
			)
			c.conn.Close()
			return
		}

		log.Infof("action: do_bet | result: success | client_id: %v",
			c.config.ID)

		err = c.receiveBetResponse()
		if err != nil {
			log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v",
				c.config.ID,
				err,
			)
			c.conn.Close()
			return
		}

		c.conn.Close()

		log.Infof("action: apuesta_enviada | result: success | dni: %v | numero: %v",
			c.config.IdNumber, c.config.BetNumber)

		// Wait a time between sending one message and the next one
		time.Sleep(c.config.LoopPeriod)
	}

	log.Infof("action: loop_finished | result: success | client_id: %v", c.config.ID)
}

func (c *Client) doBets() error {
	file, err := os.Open("../../.data/agency.csv")
	if err != nil {
		log.Errorf("action: opening_bet_file | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return err
	}
	defer file.Close()

	reader := bufio.NewReader(file)
	var batch [][]byte
	var line string

	lineIndex := 0

	for {
		log.Infof("indexn %v", lineIndex)
		if lineIndex == c.config.BatchMaxAmount {
			log.Infof("action: send_chunk | result: in_progress | chunck: %v", line)
			err := writeBetMessage(c, batch)
			if err != nil {
				log.Errorf("action: send_batch_to_server | result: fail | client_id: %v | error: %v", c.config.ID, err)
				return err
			}
			lineIndex = 0
			batch = nil
		}
		line, err = reader.ReadString('\n')
		if err != nil {
			if err == io.EOF {
				break
			}
			log.Errorf("action: reading_line | result: fail | client_id: %v | error: %v", c.config.ID, err)
			return err
		}

		message, err := formatBetLine(c, line)
		if err != nil {
			log.Errorf("action: parsing_line | result: fail | client_id: %v | error: %v", c.config.ID, err)
			break
		}
		batch = append(batch, message)
		lineIndex++
	}

	err = writeNoMoreBetsMessage(c)
	if err != nil {
		log.Errorf("action: send_batch_to_server | result: fail | client_id: %v | error: %v", c.config.ID, err)
	}
	return nil
}

func (c *Client) receiveBetResponse() error {
	return decodeBetResponse(c)
}
