package common

import (
	"bufio"
	"fmt"
)

func formatBetMessage(c *Client) string {
	return fmt.Sprintf("B;%s;%s;%s;%s;%s;%s\n", c.config.ID, c.config.Name, c.config.Surname, c.config.IDNumber, c.config.DateOfBirth, c.config.BetNumber)
}

func writeBetMessage(c *Client, message string) error {
	bytesWritten := 0

	for bytesWritten < len([]byte(message)) {
		n, err := c.conn.Write([]byte(message)[bytesWritten:])
		if err != nil {
			log.Criticalf(
				"action: writing_bytes_to_server | result: fail")
		}
		bytesWritten += n
	}
	if bytesWritten < len([]byte(message)) {
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
