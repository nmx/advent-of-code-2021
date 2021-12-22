import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class Day16Test {
    @Test
    public void q1sample1() {
        testVersionSum("8A004A801A8002F478", 16);
    }

    @Test
    public void q1sample2() {
        testVersionSum("620080001611562C8802118E34", 12);
    }

    @Test
    public void q1sample3() {
        testVersionSum("C0015000016115A2E0802F182340", 23);
    }

    @Test
    public void q1sample4() {
        testVersionSum("A0016C880162017C3686B18A3D4780", 31);
    }

    private void testVersionSum(final String input, final int versionSum) {
        final Day16 day16 = new Day16(PacketReader.fromString(input));
        day16.evaluate();
        assertEquals(versionSum, day16.getVersionSum());
    }

    @Test
    public void q2sample1() {
        testEvaluate("C200B40A82", 3);
    }

    @Test
    public void q2sample2() {
        testEvaluate("04005AC33890", 54);
    }

    @Test
    public void q2sample3() {
        testEvaluate("880086C3E88112", 7);
    }

    @Test
    public void q2sample4() {
        testEvaluate("CE00C43D881120", 9);
    }

    @Test
    public void q2sample5() {
        testEvaluate("D8005AC2A8F0", 1);
    }

    @Test
    public void q2sample6() {
        testEvaluate("F600BC2D8F", 0);
    }

    @Test
    public void q2sample7() {
        testEvaluate("9C005AC2F8F0", 0);
    }

    @Test
    public void q2sample8() {
        testEvaluate("9C0141080250320F1802104A08", 1);
    }

    private void testEvaluate(final String input, final int result) {
        assertEquals(result, new Day16(PacketReader.fromString(input)).evaluate());
    }
}
