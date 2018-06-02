
CPP = c++

OPENSSL_DIR = /usr/local/Cellar/openssl/1.0.2/

OPENSSL_INCLUDES = -I$(OPENSSL_DIR)/include/
OPENSSL_LIBDIR = -L$(OPENSSL_DIR)/lib/
OPENSSL_LIBS = -lssl -lcrypto

sechash: sechash.cpp
	$(CPP) \
		$(OPENSSL_INCLUDES) \
		$(OPENSSL_LIBDIR) \
		$(OPENSSL_LIBS) \
		sechash.cpp \
		-o sechash
