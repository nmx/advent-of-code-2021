import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class PacketReaderTest {
    @Test
    public void oneByteAligned() {
        final PacketReader reader = PacketReader.fromString("AB");
        assertEquals(0xAB, reader.read(8));
    }

    @Test
    public void oneByteAlignedSecondByte() {
        final PacketReader reader = PacketReader.fromString("FFAB");
        reader.read(8);
        assertEquals(0xAB, reader.read(8));
    }

    @Test
    public void firstNibble() {
        final PacketReader reader = PacketReader.fromString("AB");
        assertEquals(0xA, reader.read(4));
    }

    @Test
    public void secondNibble() {
        final PacketReader reader = PacketReader.fromString("AB");
        reader.read(4);
        assertEquals(0xB, reader.read(4));
    }

    @Test
    public void fourBytesAligned() {
        final PacketReader reader = PacketReader.fromString("DEADBEEF");
        assertEquals(0xDEADBEEF, reader.read(32));
    }

    @Test
    public void fourBytesAlignedStartAtSecondNibble() {
        final PacketReader reader = PacketReader.fromString("EDEADBEEFE");
        reader.read(4);
        assertEquals(0xDEADBEEF, reader.read(32));
    }

    @Test
    public void literalPacket() {
        final PacketReader reader = PacketReader.fromString("D2FE28");
        assertEquals(6, reader.readVersion());
        assertEquals(4, reader.readType());
        assertEquals(2021L, reader.readLiteral());
    }
}
