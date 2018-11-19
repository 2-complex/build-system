#include <openssl/sha.h>

#include <string>

#include <string.h>
#include <stdlib.h>
#include <stdint.h>


static const std::string base64_chars =
     "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
     "abcdefghijklmnopqrstuvwxyz"
     "0123456789+/";


static inline bool is_base64(uint8_t c)
{
    return ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || (c == '+') || (c == '/'));
}


static void base64_encode(const uint8_t* bytes_to_encode, size_t in_len, std::string& out)
{
    uint8_t char_array_3[3];
    uint8_t char_array_4[4];

    size_t i = 0;

    while (in_len--)
    {
        char_array_3[i++] = *(bytes_to_encode++);

        if( i == 3 )
        {
            char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
            char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
            char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
            char_array_4[3] = char_array_3[2] & 0x3f;

            for( i = 0; i < 4; i++ )
            {
                out += base64_chars[char_array_4[i]];
            }
            i = 0;
        }
    }

    if( i )
    {
        int j = 0;

        for( j = i; j < 3; j++ )
        {
            char_array_3[j] = '\0';
        }

        char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
        char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
        char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
        char_array_4[3] = char_array_3[2] & 0x3f;

        for( j = 0; (j < i + 1); j++ )
        {
            out += base64_chars[char_array_4[j]];
        }

        while( i++ < 3 )
        {
            out += '=';
        }
    }
}


static std::string base64_decode(std::string const& encoded_string)
{
    size_t in_len = encoded_string.size();
    size_t i = 0;
    size_t j = 0;
    size_t in_ = 0;
    uint8_t char_array_4[4];
    uint8_t char_array_3[3];
    std::string ret;

    while( in_len-- && ( encoded_string[in_] != '=') && is_base64(encoded_string[in_]) )
    {
        char_array_4[i++] = encoded_string[in_];
        in_++;

        if( i ==4 )
        {
            for( i = 0; i <4; i++ )
            {
                char_array_4[i] = base64_chars.find(char_array_4[i]);
            }

            char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
            char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
            char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

            for( i = 0; (i < 3); i++ )
            {
                ret += char_array_3[i];
            }

            i = 0;
        }
    }

    if( i )
    {
        for( j = i; j < 4; j++ )
        {
            char_array_4[j] = 0;
        }

        for( j = 0; j < 4; j++ )
        {
            char_array_4[j] = base64_chars.find(char_array_4[j]);
        }

        char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
        char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
        char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

        for( j = 0; (j < i - 1); j++ )
        {
            ret += char_array_3[j];
        }
    }

    return ret;
}

enum SecHashError
{
    NO_ERROR = 0,
    FILE_NOT_FOUND,
    FILE_NOT_FULLY_READ,
    SHA_ERROR
};

class SecHash
{
public:
    SecHash(SecHashError err)
        : err(err)
    {
    }

    SecHash(SHA512_CTX* shaContextPtr)
        : err(NO_ERROR)
    {
        if( ! SHA512_Final(bytes, shaContextPtr) )
        {
            err = SHA_ERROR;
        }
    }

    const uint8_t* getBytes() const
    {
        return bytes;
    }

    SecHashError getError() const
    {
        return err;
    }

    const char* getBase64() const
    {
        if( base64.empty() )
        {
            base64_encode(bytes, SHA512_DIGEST_LENGTH, base64);
        }

        return base64.c_str();
    }

private:
    SecHashError err;
    uint8_t bytes[SHA512_DIGEST_LENGTH];
    mutable std::string base64;
};


#include <stdio.h>

const size_t CHUNK_SIZE = 256;

SecHash hashFile(const char* filename)
{
    SHA512_CTX shaContext;
    SHA512_Init(&shaContext);

    uint8_t chunk[CHUNK_SIZE];

    FILE* fp = fopen(filename, "rb");
    if( fp )
    {
        size_t numBytesRead;
        while( (numBytesRead = fread(chunk, sizeof(uint8_t), CHUNK_SIZE, fp)) > 0 )
        {
            SHA512_Update(&shaContext, chunk, numBytesRead);
        }

        if( ferror(fp) )
        {
            return SecHash(FILE_NOT_FULLY_READ);
        }
    }
    else
    {
        return SecHash(FILE_NOT_FOUND);
    }

    return SecHash(&shaContext);
};


int main(int argc, char** args)
{
    if( argc != 2 )
    {
        fprintf(stderr, "wrong number of args, takes filepath\n");
    }
    else
    {
        SecHash hash(hashFile(args[1]));
        if( hash.getError() == NO_ERROR )
        {
            printf("%s\n", hash.getBase64());
        }
        else
        {
            switch(hash.getError())
            {
                case NO_ERROR:
                    fprintf(stderr, "What?  No error?\n");
                break;

                case FILE_NOT_FOUND:
                    fprintf(stderr, "File not found.\n");
                break;

                case FILE_NOT_FULLY_READ:
                    fprintf(stderr, "File not fully read.\n");
                break;

                case SHA_ERROR:
                    fprintf(stderr, "SHA512 computation failed.\n");
                break;

                default:
                    fprintf(stderr, "Unknown error.\n");
                break;
            }
        }

    }

    return 0;
}
