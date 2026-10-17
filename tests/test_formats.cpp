// Tests C++ sur ordinateur, lancés par tools/test_host.py. Le WAV est ensuite relu par Python.
#include "LabFormats.h"
#include <assert.h>
#include <fstream>
int main(int argc, char** argv) {
    assert(argc == 2);
    uint8_t header[44]; Lab::wavHeader(header, 32000, 16000);
    std::ofstream output(argv[1], std::ios::binary);
    output.write(reinterpret_cast<char*>(header), sizeof(header));
    char silence[32000] = {}; output.write(silence, sizeof(silence)); output.close();
    // Parcourir les 256 numéros de blocs vérifie que seul le bloc 4 reste inscriptible.
    for (unsigned i = 0; i < 256; ++i) assert(Lab::writableLabBlock(i) == (i == 4));
    // Contrôler un paquet valide, une taille tronquée, une signature erronée et un texte sans zéro final.
    Lab::Packet packet = {}, decoded = {}; packet.magic = Lab::PACKET_MAGIC;
    strcpy(packet.text, "test");
    assert(Lab::decodePacket(reinterpret_cast<uint8_t*>(&packet), sizeof(packet), decoded));
    assert(!Lab::decodePacket(reinterpret_cast<uint8_t*>(&packet), sizeof(packet) - 1, decoded));
    packet.magic = 0;
    assert(!Lab::decodePacket(reinterpret_cast<uint8_t*>(&packet), sizeof(packet), decoded));
    packet.magic = Lab::PACKET_MAGIC; memset(packet.text, 'a', sizeof(packet.text));
    assert(!Lab::decodePacket(reinterpret_cast<uint8_t*>(&packet), sizeof(packet), decoded));
}
