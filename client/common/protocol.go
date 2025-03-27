package common

import (
	"bufio"
	"fmt"
	"strings"
)

func formatBetLine(c *Client, line string) ([]byte, error) {
	fields := strings.Split(strings.TrimSpace(line), ",")

	if len(fields) != 5 {
		return nil, fmt.Errorf("insuficient fields")
	}
	message := fmt.Sprintf("B;%s;%s;%s;%s;%s;%s\n", c.config.ID, fields[0], fields[1], fields[2], fields[3], fields[4])
	return []byte(message), nil
}

func writeBetMessage(c *Client, message []byte) error {
	bytesWritten := 0
	totalBytes := len(message)

	for bytesWritten < totalBytes {
		n, err := c.conn.Write(message[bytesWritten:])
		if err != nil {
			log.Criticalf(
				"action: writing_bytes_to_server | result: fail")
			return err
		}
		bytesWritten += n
	}
	if bytesWritten < len(message) {
		log.Criticalf(
			"action: writing_bet_to_server | result: fail")
	}
	return nil
}

func decodeBetResponse(c *Client) error {
	msg, err := bufio.NewReader(c.conn).ReadString('\n')
	if err != nil {
		log.Criticalf("action: reading_bet_response | result: fail | error: %v", err)
	}
	if len(msg) > 0 && msg[0] == 'E' {
		log.Criticalf("action: reading_bet_response | result: fail")
	}

	log.Infof("action: reading_bet_response | result: success | msg: %v", msg)
	return nil
}
