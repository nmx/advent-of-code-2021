import com.google.common.collect.ImmutableMap;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.function.ToLongFunction;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkState;

public class Day16 {
    private static final int TYPE_LITERAL = 4;
    private static final Map<Integer, ToLongFunction<List<Long>>> operators = ImmutableMap.of(
            0, Day16::sum,
            1, Day16::product,
            2, Day16::min,
            3, Day16::max,
            5, Day16::gt,
            6, Day16::lt,
            7, Day16::eq
    );

    private static final int LENGTH_TYPE_BITS = 0;
    private static final int LENGTH_TYPE_PACKETS = 1;

    private final PacketReader packetReader;
    private long versionSum;

    public static void main(final String[] args) throws IOException {
        final Day16 day16 = new Day16(PacketReader.fromFile("input.txt"));
        long res = day16.evaluate();
        System.out.println("Q1 (version sum): " + day16.getVersionSum());
        System.out.println("Q2 (evaluation): " + res);
    }

    public Day16(final PacketReader packetReader) {
        this.packetReader = packetReader;
    }

    public long getVersionSum() {
        return versionSum;
    }

    public long evaluate() {
        return evaluatePacket(); /* single outer packet */
    }

    private long evaluatePacket() {
        versionSum += packetReader.readVersion();
        final int typeId = packetReader.readType();
        final long result;
        if (typeId == TYPE_LITERAL) {
            result = packetReader.readLiteral();
        } else {
            // Operator
            final int lengthTypeId = packetReader.readLengthType();
            final List<Long> operands;
            if (lengthTypeId == LENGTH_TYPE_BITS) {
                final int bitCount = packetReader.readBitCount();
                final int destPos = packetReader.getPos() + bitCount;
                operands = evaluatePackets(new PosMode(destPos));
            } else if (lengthTypeId == LENGTH_TYPE_PACKETS) {
                final int packetCount = packetReader.readPacketCount();
                operands = evaluatePackets(new PacketsMode(packetCount));
            } else {
                throw new IllegalArgumentException("unknown length type ID " + lengthTypeId);
            }
            result = operators.get(typeId).applyAsLong(operands);
        }
        checkState(result >= 0);
        return result;
    }

    private List<Long> evaluatePackets(final SubPacketMode subPacketMode) {
        final List<Long> operands = new ArrayList<>();
        do {
            operands.add(evaluatePacket());
        } while (subPacketMode.morePackets());
        return operands;
    }

    private interface SubPacketMode {
        boolean morePackets();
    }

    private class PosMode implements SubPacketMode {
        final int pos;

        public PosMode(final int pos) {
            this.pos = pos;
        }

        @Override
        public boolean morePackets() {
            return packetReader.getPos() < pos;
        }
    }

    private static class PacketsMode implements SubPacketMode {
        int packetsLeft;

        public PacketsMode(final int packets) {
            packetsLeft = packets;
        }

        @Override
        public boolean morePackets() {
            return --packetsLeft > 0;
        }
    }

    private static long sum(final List<Long> operands) {
        return operands.stream().mapToLong(Long::longValue).sum();
    }

    private static long product(final List<Long> operands) {
        return operands.stream().reduce(1L, (i, j) -> i * j);
    }

    private static long min(final List<Long> operands) {
        return operands.stream().mapToLong(Long::longValue).min().orElseThrow(NoSuchElementException::new);
    }

    private static long max(final List<Long> operands) {
        return operands.stream().mapToLong(Long::longValue).max().orElseThrow(NoSuchElementException::new);
    }

    private static long gt(final List<Long> operands) {
        checkArgument(operands.size() == 2);
        return operands.get(0) > operands.get(1) ? 1 : 0;
    }

    private static long lt(final List<Long> operands) {
        checkArgument(operands.size() == 2);
        return operands.get(0) < operands.get(1) ? 1 : 0;
    }

    private static long eq(final List<Long> operands) {
        checkArgument(operands.size() == 2);
        return operands.get(0).equals(operands.get(1)) ? 1 : 0;
    }
}
