package tokens

import "crypto/rand"

func cryptoRandRead(p []byte) (int, error) { return rand.Read(p) }

// RandFill fills p from crypto/rand.
func RandFill(p []byte) { rand.Read(p) }
