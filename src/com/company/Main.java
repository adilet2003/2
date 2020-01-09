package com.company;

public class Main {
    public static int bossHeelth = 700;
    public static int bossDamage = 50;
    public static String bossDefensType = "";
    public static int docturHealth = 450;
    public static int docturhilse = 20;
    public static String hilse = " hil";
    public static int[] heroesHealth = {250, 250, 250};
    public static int[] heroesDemage = {20, 20, 20};
    public static String[] heroesAttactype = {" Physical", " Magical", " Mental"};


    public static void main(String[] args) {
        while (!isFinehed()) {
            раунд();
        }
    }

    public static void раунд() {
        bossHit();
        heroesHit();
        docturHil();
        статистика();
    }


    public static boolean isFinehed() {
        if (bossHeelth <= 0) {
            System.out.println(" герой победил!!!");
            return true;
        }
        if (docturHealth <= 0) {
            System.out.println(" boss won!!!");
            return true;
        }
        if (heroesHealth[0] <= 0 && heroesHealth[1] <= 0 && heroesHealth[2] <= 0) {
            System.out.println("boss won!!!");
            return true;
        }
        return false;

    }

    public static void bossHit() {
        for (int i = 0; i <  heroesHealth.length; i++) {
            heroesHealth[i] = heroesHealth[i] - bossDamage;

        }
            docturHealth = docturHealth - bossDamage;

    }

    public static void docturHil() {
        for (int i = 0; i < heroesHealth.length; i++) {
            heroesHealth[i] = heroesHealth[i] + docturhilse;

        }
    }

    public static void heroesHit() {
        for (int i = 0; i < heroesDemage.length; i++) {
            bossHeelth = bossHeelth - heroesDemage[i];

        }
    }

    public static void статистика() {
        System.out.println("_________________________________________________");
        System.out.println(" boss health: " + bossHeelth);
        System.out.println(" warrior health: " + heroesHealth[0]);
        System.out.println(" megic health: " + heroesHealth[1]);
        System.out.println(" kinetic health: " + heroesHealth[2]);
        System.out.println(" doctur health: " + docturHealth);
        System.out.println("_________________________________________________");
    }


}

