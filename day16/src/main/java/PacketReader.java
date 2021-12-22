import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.NoSuchElementException;

public class PacketReader {
    // Not being concerned about space efficiency, since the packets are densely packed, with fields not being aligned
    // on byte boundaries, it's easier to actually store each bit as a '1' or '0' to avoid a lot of bit shifting.
    private final byte[] bytes;
    private int pos;

    public static PacketReader fromFile(final String filename) throws IOException {
        return fromString(Files.readString(Path.of(filename)).trim());
    }

    public static PacketReader fromString(final String content) {
        if (content.length() % 2 != 0) {
            throw new IllegalArgumentException("content must be aligned on a byte boundary");
        }
        byte[] bytes = new byte[content.length() / 2];
        for (int i = 0; i < content.length(); i += 2) {
            bytes[i / 2] = (byte) (Integer.parseInt(content.substring(i, i + 2), 16) & 0xFF);
        }
        return new PacketReader(bytes);
    }

    public PacketReader(final byte[] bytes) {
        this.bytes = bytes;
    }

    public void reset() {
        pos = 0;
    }

    public int getPos() {
        return pos;
    }

    public boolean isEof() {
        // need at least two bytes
        return pos / 8 >= bytes.length - 1;
    }

    public int read(final int numBits) {
        if ((pos + numBits) / 8 > bytes.length)
            throw new NoSuchElementException("would read past end of buffer");
        if (numBits > 32)
            throw new IllegalArgumentException("can read at most 32 bits at a time");

        int res = 0;
        int curByte = pos / 8;
        int bitsRemaining = numBits;

        int startBitInByte = pos % 8;

        while (bitsRemaining > 0) {
            int bitsToReadFromByte = Math.min(bitsRemaining, 8 - startBitInByte);
            int thisByte = 0xff & bytes[curByte];

            // lose high order bits we don't want
            thisByte = (thisByte << startBitInByte) & 0xFF;

            // shift into position
            thisByte >>>= (8 - bitsToReadFromByte);

            res = (res << bitsToReadFromByte) | thisByte;
            bitsRemaining -= bitsToReadFromByte;

            curByte++;
            startBitInByte = 0;
        }

        pos += numBits;
        return res;
    }

    public int readVersion() {
        return read(3);
    }

    public int readType() {
        return read(3);
    }

    public int readLengthType() {
        return read(1);
    }

    public int readBitCount() {
        return read(15);
    }

    public int readPacketCount() {
        return read(11);
    }

    public long readLiteral() {
        long res = 0;

        while (true) {
            final int segment = read(5);
            res = (res << 4) | (segment & 0xF);
            if ((segment & 0x10) == 0) {
                break;
            }
        }

        return res;
    }
}
