package main

// #include <stdlib.h>
import "C"
import (
	"unsafe"
	"os"
	"encoding/base64"
	"fmt"
	"encoding/json"
	verifier "github.com/minvws/nl-covid19-coronacheck-mobile-core"
	mobilecore "github.com/minvws/nl-covid19-coronacheck-mobile-core"
)

//export test
func test() int {
	return 1
}

//export ffiverify
func ffiverify(proofQREncoded *C.char, configpath *C.char) *C.char {
	mobilecore.InitializeVerifier(C.GoString(configpath))
	res, _ := json.Marshal(verifier.Verify([]byte(C.GoString(proofQREncoded))))

	ret := C.CString(string(res))
	//defer C.free(unsafe.Pointer(ret))
	//defer C.free(unsafe.Pointer(proofQREncoded))
	//defer C.free(unsafe.Pointer(configpath))

	return ret
}

//export freeCString
func freeCString(s *C.char) {
        C.free(unsafe.Pointer(s))
}

func main() {
	arg := os.Args[1]
	b64res, _ := base64.StdEncoding.DecodeString(arg)

	mobilecore.InitializeVerifier("./config/")
	res, _ := json.Marshal(verifier.Verify(b64res))

	fmt.Println(string(res))
}
